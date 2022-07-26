import logging
import os
import tempfile
import uuid
from io import StringIO
from os.path import join, dirname

import telegram
from dotenv import load_dotenv
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from solver.screenshot_cv import ScreenshotCV
from solver.solution_finder import SolutionFinder
from solver.solution_printer import SolutionPrinter
from solver.solution_printer_stepped import SolutionPrinterStepped

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

ANSWER = 0
SOLUTION = 'SOLUTION'


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
            analyzer = ScreenshotCV(file_name)
            update.message.reply_text(
                'Processing was started.',
            )
            analyzer.analyze()
            solver = SolutionFinder(analyzer.field)
            solver.solve()
        except Exception as err:
            update.message.reply_text(
                'Exception was found. Exception msg: {}'.format(err.args),
                reply_markup=ReplyKeyboardMarkup(reply_keyboard),
            )
            return ConversationHandler.END

    if solver.is_solved:
        update.message.reply_text(
            'Answer was found. To navigate use text command or keyboard',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard),
        )
        print_step_list = SolutionPrinter(solver.field, solver.solved_way)
        print_step_list.build()

        context.user_data[SOLUTION] = solution = SolutionPrinterStepped(print_step_list)
        reply_with_step(update, solution)
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


def reply_with_step(update, solution):
    str_io = StringIO()
    solution.print(str_io)
    update.message.reply_text(
        text='<pre>{}</pre>'.format(str_io.getvalue()),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard),
        parse_mode=telegram.ParseMode.HTML
    )


def answer(update: Update, context):
    solution: SolutionPrinterStepped = context.user_data[SOLUTION]
    if update.message.text == '/forward':
        solution.increment()
    elif update.message.text == '/backward':
        solution.decrement()
    elif update.message.text == '/begin':
        solution.begin()
    elif update.message.text == '/end':
        del context.user_data[SOLUTION]
        update.message.reply_text(
            'Bye Bye',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    reply_with_step(update, solution)
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
