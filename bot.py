import tempfile

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
from image_solver import ImageSolver
import uuid
import os
from os.path import join, dirname
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

ANSWER = 0


def start(update, _: CallbackContext):
    update.message.reply_text('Бот для решения паззла BallSortPuzzle ')


def echo(update: Update, _: CallbackContext):
    """Echo the user message."""
    print(update.message)


reply_keyboard = [
    ['/forward', '/backward', '/begin', '/end'],
]


def to_solve(update: Update, context: CallbackContext):
    effective_attachment = update.effective_message.effective_attachment
    if isinstance(effective_attachment, list):
        file_id = effective_attachment[-1].file_id
    else:
        file_id = effective_attachment.file_id
    file = context.bot.get_file(file_id)

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_name = os.path.join(tmp_dir, str(uuid.uuid4()))
        file.download(file_name)
        try:
            solver = ImageSolver(file_name)
            update.message.reply_text(
                'Processing was started.',
            )
            is_solved = solver.solve()
        except Exception as err:
            update.message.reply_text(
                'Exception was found. Exception msg: {}'.format(err.args),
                reply_markup=ReplyKeyboardMarkup(reply_keyboard),
            )
            return ConversationHandler.END

    context.user_data['way'] = solver.way
    context.user_data['index'] = 0

    if is_solved:
        update.message.reply_text(
            'Answer was found. To navigate use text command or keyboard',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard),
        )
        print_current(update, solver.way, 0)

        return ANSWER
    else:
        update.message.reply_text(
            'Solution is not found.',
        )

        return ConversationHandler.END


def cancel(update: Update, _):
    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def flask_to_str(source):
    return f'{source % 7 + 1}{"↑" if source // 7 == 1 else "↓"}'


def print_current(update, way, index):
    s, t, c = way[index]
    update.message.reply_text(
        text='From {} to {}. Step {} from {}'.format(
            flask_to_str(s),
            flask_to_str(t),
            index + 1,
            len(way)
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard),
    )


def answer(update: Update, context):
    way = context.user_data['way']
    index = context.user_data['index']

    if update.message.text == '/forward':
        if index < len(way):
            index += 1
    elif update.message.text == '/backward':
        if index > 0:
            index -= 1
    elif update.message.text == '/begin':
        index = 0
    elif update.message.text == '/end':
        update.message.reply_text(
            'Bye Bye',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    context.user_data['index'] = index
    print_current(update, way, index)
    return ANSWER


def main():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    updater = Updater(os.environ.get('token'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.photo | Filters.document.mime_type("image/jpeg") & ~Filters.command, to_solve)],
            states={
                ANSWER: [
                    MessageHandler(Filters.regex('^/(forward|backward|begin|end)$'), answer),
                ]
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
