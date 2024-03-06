import cv2
from typing import List
from collections import defaultdict
from copy import deepcopy


class Problem:
    def __init__(self, func=None):
        self.Solve = func


def problem(func):
    return Problem(func)


class Q1:
    def __init__(self):
        self.images = []
        self.grayScaled = []
        for i in range(1, 4):
            self.images.append(cv2.imread('./images/img' + str(i) + '.png'))

        @problem
        def P1():
            imgs = deepcopy(self.images)
            for i in range(3):
                for row in imgs[i]:
                    for pixel in row:
                        # BGR
                        grayScale = 0.11 * pixel[0] + \
                            0.59 * pixel[1] + 0.3 * pixel[2]
                        pixel[0] = grayScale
                        pixel[1] = grayScale
                        pixel[2] = grayScale
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q1-1.png', imgs[i])
            self.grayScaled = imgs
        self.P1 = P1

        @problem
        def P2():
            imgs = deepcopy(self.grayScaled)
            thresh = 128
            for i in range(3):
                for row in imgs[i]:
                    for pixel in row:
                        if pixel[0] > thresh:
                            pixel[0] = 255
                            pixel[1] = 255
                            pixel[2] = 255
                        else:
                            pixel[0] = 0
                            pixel[1] = 0
                            pixel[2] = 0
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q1-2.png', imgs[i])
        self.P2 = P2

        @problem
        def P3():
            MAX_COLORS = 16
            imgs = deepcopy(self.images)
            for i in range(3):
                colors = defaultdict(int)
                for row in imgs[i]:
                    for pixel in row:
                        rgb = pixel[0] << 16 | pixel[1] << 8 | pixel[2]
                        colors[rgb] += 1
                sortedColors = sorted(
                    colors.items(), key=lambda x: x[1], reverse=True)
                sortedColors = [colorPair[0]
                                for colorPair in sortedColors[:MAX_COLORS]]
                for row in imgs[i]:
                    for pixel in row:
                        rgb = pixel[0] << 16 | pixel[1] << 8 | pixel[2]
                        minDiff = float('inf')
                        index = -1
                        for j in range(MAX_COLORS):
                            diff = abs(rgb - sortedColors[j])
                            if diff < minDiff:
                                minDiff = diff
                                index = j
                        pixel[0] = sortedColors[index] >> 16
                        pixel[1] = (sortedColors[index] >> 8) & 0xFF
                        pixel[2] = sortedColors[index] & 0xFF
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q1-3.png', imgs[i])

        self.P3 = P3

    def Solve(self):
        # self.P1.Solve()
        # self.P2.Solve()
        self.P3.Solve()


if __name__ == '__main__':
    q1 = Q1()
    q1.Solve()
    print('Done')
