import cv2
import math
import task
import glob
import os


def analise(path):
    image = cv2.imread(path)
    image = image[375:940]
    half_height = image.shape[0] / 2
    width = image.shape[1]

    trans_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    trans_image = cv2.GaussianBlur(trans_image, (7, 7), 0)
    trans_image = cv2.threshold(trans_image, 64, 255, cv2.THRESH_BINARY)[1]

    contours, hierarchy = cv2.findContours(trans_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    vis = image.copy()
    cv2.drawContours(vis, contours, -1, (0, 255, 0), 1, cv2.LINE_AA, hierarchy, 2)

    points = []
    mapped = {}

    def cie76(c1, c2):
        return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2) + math.pow(c1[2] - c2[2], 2))

    def is_knew(pix):
        for i in mapped.keys():
            if cie76(i, pix) < 15:
                return i

    for cnt in contours:
        M = cv2.moments(cnt)
        x = int(M["m10"] / M["m00"] / 2 * 2)
        y = int(M["m01"] / M["m00"] / 2 * 2)

        pixel = image[y, x]
        pixel = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
        knew = is_knew(pixel)
        if not knew:
            index = mapped[tuple(pixel)] = len(mapped)
        else:
            index = mapped[knew]

        points.append((x, y, chr(index + ord('A'))))

    def comparator(x):
        return x[0] + (0 if x[1] < half_height else width), -x[1]

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    points.sort(key=comparator)

    inpt = list(chunks(list(map(lambda x: x[2], points)), 4))
    inpt.extend([[], []])

    way = task.find_way(inpt)

    return way
    # task.print_solution(inpt, way)


if __name__ == '__main__':
    files = glob.glob('*.jpg')
    files.sort(key=lambda x: os.path.getctime(x))

    analise(files[-1])
