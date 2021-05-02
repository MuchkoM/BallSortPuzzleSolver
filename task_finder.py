import glob
import math
import os
import sys
import cv2

import task_solver


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


def analise(path, show_vis=None):
    image = cv2.imread(path)

    height = image.shape[0]
    start_height = height // 10
    end_height = height - start_height

    image = image[start_height:end_height]

    trans_image = image.copy()
    vis = trans_image.copy()
    trans_image = cv2.cvtColor(trans_image, cv2.COLOR_BGR2GRAY)
    trans_image = cv2.GaussianBlur(trans_image, (7, 7), 0)
    trans_image = cv2.threshold(trans_image, 64, 255, cv2.THRESH_BINARY)[1]

    contours, hierarchy = cv2.findContours(trans_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def cie76(c1, c2):
        return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2) + math.pow(c1[2] - c2[2], 2))

    def is_knew(pix):
        for i in mapped.keys():
            if cie76(i, pix) < 15:
                return i

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = 0, 0, 0
    res = hierarchy_analyser(hierarchy[0])

    points = []
    mapped = {}
    for i, col in enumerate(res):
        if not len(col):
            continue
        for j, el in enumerate(col):
            contour = contours[el]

            moments = cv2.moments(contour)
            x = int(moments["m10"] / moments["m00"] / 3 * 3)
            y = int(moments["m01"] / moments["m00"] / 3 * 3)

            pixel = image[y, x]
            pixel = int(pixel[0]), int(pixel[1]), int(pixel[2])
            knew = is_knew(pixel)
            if not knew:
                index = mapped[pixel] = len(mapped)
            else:
                index = mapped[knew]

            point = x, y, chr(index + ord('A'))

            if show_vis:
                cv2.putText(vis, point[2], (point[0] - 10, point[1] + 10), font, 1, color, 2)

            res[i][j] = point

            points.append(point)

    if show_vis:
        cv2.drawContours(vis, contours, -1, (0, 0, 255))
        cv2.imshow('image', vis)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    for col in res:
        col.sort(key=lambda val: -val[1])

    def comp(column):
        if len(column) > 0:
            return column[0][1], column[0][0]
        else:
            return math.inf, math.inf

    res.sort(key=comp)

    for i, col in enumerate(res):
        if not len(col):
            continue
        for j, el in enumerate(col):
            res[i][j] = el[2]

    return res


if __name__ == '__main__':
    files = glob.glob('*.jpg')
    files.sort(key=lambda x: os.path.getctime(x))

    task = analise(files[-1], sys.argv[1] if len(sys.argv) > 1 else None)
    task_solver.printer(task)
