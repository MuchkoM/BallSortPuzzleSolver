import math

import cv2

from solver.field import Field
from solver.field_printer import FieldPrinter
from solver.palette import Palette
from solver.utils import get_int_color, get_file, map2d


# text_color = 0, 0, 0
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(vis, str(element[2]), (element[0] - 10, element[1] + 10), font, 1, text_color, 2)

# cv2.drawContours(vis, contours, -1, (0, 0, 255))
# cv2.imshow('image', vis)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
def hierarchy_analyser(hierarchy):
    out_contour = 0
    result = []

    while True:
        if out_contour == -1:
            break
        result.append([])
        in_contour = hierarchy[out_contour][2]
        in_contour = hierarchy[in_contour][2]

        if in_contour != -1:
            while True:
                if in_contour == -1:
                    break
                result[-1].append(in_contour)
                in_contour = hierarchy[in_contour][0]
        out_contour = hierarchy[out_contour][0]

    return result


def build_element(contour, image, palette):
    moments = cv2.moments(contour)
    x = int(moments["m10"] / moments["m00"] / 3 * 3)
    y = int(moments["m01"] / moments["m00"] / 3 * 3)

    pixel = image[y, x]
    color = get_int_color(pixel)

    return x, y, palette.get_index_by_color(color)


def build_contours(image):
    trans_image = image.copy()
    trans_image = cv2.cvtColor(trans_image, cv2.COLOR_BGR2GRAY)
    trans_image = cv2.GaussianBlur(trans_image, (7, 7), 0)
    trans_image = cv2.threshold(trans_image, 64, 255, cv2.THRESH_BINARY)[1]

    return cv2.findContours(trans_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


def resize_image(image):
    height = image.shape[0]
    start_height = height // 10
    end_height = height - start_height

    return image[start_height:end_height]


def comp(column):
    if len(column) > 0:
        return column[0][1], column[0][0]
    else:
        return math.inf, math.inf


class ScreenshotCV:
    def __init__(self, path):
        self.path = path
        self.field = None
        self.palette = None

    def analyze(self):
        image = resize_image(cv2.imread(self.path))
        contours, hierarchy = build_contours(image)
        self.palette = Palette()
        res = hierarchy_analyser(hierarchy[0])
        res = map2d(lambda x: build_element(contours[x], image, self.palette), res)
        res = sorted(res, key=comp)
        res = map2d(lambda x: x[2], res)
        self.field = Field(res)


if __name__ == '__main__':
    analyzer = ScreenshotCV(get_file())
    analyzer.analyze()
    printer = FieldPrinter(analyzer.field, analyzer.palette)
    printer.print()
