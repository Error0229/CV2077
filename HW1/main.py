import cv2
from typing import List
from collections import defaultdict
from copy import deepcopy
import numpy as np


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

        @problem
        def P3ALTER():
            MAX_COLORS = 16
            CLUSTERS = 4  # cause there are three colors, 4 * 4 * 4 => 64
            DIV = 256//CLUSTERS
            imgs = deepcopy(self.images)

            for i in range(3):
                colors = defaultdict(int)
                for row in imgs[i]:
                    for pixel in row:
                        rgb = (pixel[0]//DIV) << 16 | \
                            (pixel[1]//DIV) << 8 | (pixel[2]//DIV)
                        colors[rgb] += 1
                sortedColors = sorted(
                    colors.items(), key=lambda x: x[1], reverse=True)
                sortedColors = [colorPair[0]
                                for colorPair in sortedColors[:MAX_COLORS]]
                for row in imgs[i]:
                    for pixel in row:
                        rgb = (pixel[0]//DIV) << 16 | \
                            (pixel[1]//DIV) << 8 | (pixel[2]//DIV)
                        minDiff = float('inf')
                        index = -1
                        for j in range(min(MAX_COLORS, len(sortedColors))):
                            diff = abs(rgb - sortedColors[j])
                            if diff < minDiff:
                                minDiff = diff
                                index = j
                        pixel[0] = (sortedColors[index] >> 16)*DIV
                        pixel[1] = ((sortedColors[index] >> 8) & 0xFF)*DIV
                        pixel[2] = (sortedColors[index] & 0xFF)*DIV
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q1-3.png', imgs[i])
        self.P3ALTER = P3ALTER

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()
        # self.P3.Solve()
        self.P3ALTER.Solve()


class Q2():
    def __init__(self):
        self.images = []
        for i in range(1, 4):
            self.images.append(cv2.imread('./images/img' + str(i) + '.png'))

        @problem
        def P1():
            """
            Resizing image to 1/2 and 2 times without interpolation
            """
            imgs = deepcopy(self.images)
            for i in range(3):
                # create a empty image with 2 times the size
                result = np.zeros(
                    (imgs[i].shape[0]*2, imgs[i].shape[1]*2, 3), dtype=np.uint8)
                for row in range(imgs[i].shape[0]):
                    for col in range(imgs[i].shape[1]):
                        result[row*2, col*2] = imgs[i][row, col]
                        result[row*2, col*2+1] = imgs[i][row, col]
                        result[row*2+1, col*2] = imgs[i][row, col]
                        result[row*2+1, col*2+1] = imgs[i][row, col]
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q2-1-double.png', result)
                result = np.zeros(
                    (imgs[i].shape[0]//2, imgs[i].shape[1]//2, 3), dtype=np.uint8)
                for row in range(result.shape[0]):
                    for col in range(result.shape[1]):
                        result[row, col] = (imgs[i][row*2, col*2])
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q2-1-half.png', result)
        self.P1 = P1

        @problem
        def P2():
            """
            Resizing image to 1/2 and 2 times with Bilinear interpolation
            """
            imgs = deepcopy(self.images)
            imgs = [img.astype(np.float32) for img in imgs]
            for i in range(3):
                # create a empty image with 2 times the size
                result = np.zeros(
                    (imgs[i].shape[0]*2, imgs[i].shape[1]*2, 3), dtype=np.float32)
                for row in range(result.shape[0]):
                    for col in range(result.shape[1]):
                        x = col//2
                        y = row//2
                        x1 = x+1 if x+1 < imgs[i].shape[1] else x
                        y1 = y+1 if y+1 < imgs[i].shape[0] else y
                        result[row, col] = (imgs[i][y, x] + imgs[i][y, x1] +
                                            imgs[i][y1, x] + imgs[i][y1, x1])/4
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q2-2-double.png', result.astype(np.uint8))

                result = np.zeros(
                    (imgs[i].shape[0]//2, imgs[i].shape[1]//2, 3), dtype=np.float32)
                for row in range(result.shape[0]):
                    for col in range(result.shape[1]):
                        x = col*2
                        y = row*2
                        result[row, col] = (imgs[i][y, x] + imgs[i][y, x+1] +
                                            imgs[i][y+1, x] + imgs[i][y+1, x+1])/4
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q2-2-half.png', result.astype(np.uint8))
        self.P2 = P2

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()


if __name__ == '__main__':
    q1 = Q1()
    q2 = Q2()
    q1.Solve()
    q2.Solve()
    print('Done')
