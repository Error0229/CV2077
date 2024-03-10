import cv2
from typing import List
from collections import defaultdict
from copy import deepcopy
import numpy as np
from cv2.typing import MatLike


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
                            r = (sortedColors[j] >> 16)*DIV
                            g = ((sortedColors[j] >> 8) & 0xFF)*DIV
                            b = (sortedColors[j] & 0xFF)*DIV
                            diff = abs(r-pixel[0]) + \
                                abs(g-pixel[1]) + abs(b-pixel[2])
                            if diff < minDiff:
                                minDiff = diff
                                index = j
                        pixel[0] = (sortedColors[index] >> 16)*DIV
                        pixel[1] = ((sortedColors[index] >> 8) & 0xFF)*DIV
                        pixel[2] = (sortedColors[index] & 0xFF)*DIV
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q1-3.png', imgs[i])
        self.P3ALTER = P3ALTER

        @problem
        def P3077():
            MAX_COLORS = 16
            THRESH = 30
            DIVS = 4
            imgs = [img.astype(np.float32) for img in self.images]
            for id, img in enumerate(imgs):
                colors = []

                def CloseEnough(color):
                    for c in colors:
                        if np.linalg.norm(c-color) < THRESH:
                            return True
                    return False
                width, height, _ = img.shape
                for i in range(width // DIVS):
                    for j in range(height // DIVS):
                        pixels = img[i*DIVS:(i+1)*DIVS, j*DIVS:(j+1)*DIVS]
                        avg = np.mean(pixels, axis=(0, 1))
                        if not CloseEnough(avg):
                            colors.append(avg)
                print(len(colors))
                # color elimination by repeating increasing the threshold
                thresh = THRESH
                while len(colors) > MAX_COLORS:
                    thresh += 0.1
                    newColors = []
                    for color in colors:
                        flag = True
                        for c in colors:
                            if c is not color and np.linalg.norm(c-color) < thresh:
                                flag = False
                                break
                        if flag:
                            newColors.append(color)
                    colors = newColors

                print(len(colors))
                for i in range(width):
                    for j in range(height):
                        pixel = img[i, j]
                        minDiff = float('inf')
                        index = -1
                        for k in range(len(colors)):
                            diff = np.linalg.norm(colors[k]-pixel)
                            if diff < minDiff:
                                minDiff = diff
                                index = k
                        img[i, j] = colors[index]
                cv2.imwrite('./results/img' + str(id + 1) +
                            '_q1-3.png', img.astype(np.uint8))
            # pool from nearing colors, and insert into colors if there does not exist a color that is too close
        self.P3077 = P3077

        @problem
        def P3000():
            MAX_COLORS = 16
            THRESH = 5
            DIVS = 4
            imgs = [img.astype(np.float32) for img in self.images]
            for id, img in enumerate(imgs):
                colors = []

                def CloseEnough(color, flag=False, thresh=THRESH):
                    for c in colors:
                        if flag and c is color:
                            continue
                        if abs(c[0]-color[0]) < thresh and abs(c[1]-color[1]) < thresh and abs(c[2]-color[2]) < thresh:
                            return True
                    return False
                width, height, _ = img.shape
                for i in range(width // DIVS):
                    for j in range(height // DIVS):
                        pixels = img[i*DIVS:(i+1)*DIVS, j*DIVS:(j+1)*DIVS]
                        avg = np.mean(pixels, axis=(0, 1))
                        if not CloseEnough(avg):
                            colors.append(avg)
                print(len(colors))
                # color elimination by repeating increasing the threshold
                thresh = THRESH
                while len(colors) > MAX_COLORS:
                    thresh += 0.05
                    newColors = []
                    for color in colors:
                        if not CloseEnough(color, True, thresh):
                            newColors.append(color)
                    colors = newColors

                print(len(colors))
                for i in range(width):
                    for j in range(height):
                        pixel = img[i, j]
                        minDiff = float('inf')
                        index = -1
                        for k in range(len(colors)):
                            diff = abs(
                                pixel[0]-colors[k][0]) + abs(pixel[1]-colors[k][1]) + abs(pixel[2]-colors[k][2])
                            if diff < minDiff:
                                minDiff = diff
                                index = k
                        img[i, j] = colors[index]
                cv2.imwrite('./results/img' + str(id + 1) +
                            '_q1-3.png', img.astype(np.uint8))
            # pool from nearing colors, and insert into colors if there does not exist a color that is too close
        self.P3000 = P3000

        @problem
        def P33():
            MAX_COLORS = 16
            THRESH = 50
            DIVS = 2
            imgs = [img.astype(np.float32) for img in self.images]

            def CloseEnough(color1, color2, flag=False, thresh=THRESH):
                if abs(color1[0]-color2[0]) < thresh and abs(color1[1]-color2[1]) < thresh and abs(color1[2]-color2[2]) < thresh:
                    return True
                return False
            for id, img in enumerate(imgs):
                width, height, _ = img.shape
                colorPool = []
                for i in range(width // DIVS):
                    for j in range(height // DIVS):
                        pixels = img[i*DIVS:(i+1)*DIVS, j*DIVS:(j+1)*DIVS]
                        avg = np.mean(pixels, axis=(0, 1))
                        rgb = (avg[0].astype(np.uint16)) << 16 | \
                            (avg[1].astype(np.uint16)) << 8 | (
                                avg[2].astype(np.uint16))
                        flag = True
                        for colors in colorPool:
                            mainColor = colors[0]
                            if CloseEnough(mainColor, avg, False, THRESH):
                                flag = False
                                colors[1][rgb] += 1
                                break
                        if flag:
                            colorPool.append([avg, defaultdict(int)])
                            colorPool[-1][1][rgb] += 1
                for color in colorPool:
                    tmp = sorted(color[1].items(),
                                 key=lambda x: x[1], reverse=True)
                    # print([hex(color[0]) for color in tmp[:MAX_COLORS]])
                    color[1] = None
                    color[1] = [colorPair[0]
                                for colorPair in tmp[:MAX_COLORS]]
                colors = []
                poolID = 0
                print(f"poolcount {len(colorPool)}")
                while len(colors) < MAX_COLORS:
                    try:
                        colors.append(colorPool[poolID][1][0])
                    except:
                        poolID = (poolID + 1) % len(colorPool)
                    colorPool[poolID][1].pop(0)
                    poolID = (poolID + 1) % len(colorPool)
                # print color in hex format
                # print([hex(color) for color in colors])
                for i in range(width):
                    for j in range(height):
                        pixel = img[i, j]
                        minDiff = float('inf')
                        index = -1
                        for k in range(len(colors)):
                            r = (colors[k] >> 16) & 0xFF
                            g = (colors[k] >> 8) & 0xFF
                            b = colors[k] & 0xFF
                            diff = abs(
                                pixel[0]-r) + abs(pixel[1]-g) + abs(pixel[2]-b)
                            if diff < minDiff:
                                minDiff = diff
                                index = k
                        img[i, j] = [((colors[index] >> 16) & 0xFF), (
                            (colors[index] >> 8) & 0xFF), (colors[index] & 0xFF)]
                cv2.imwrite('./results/img' + str(id + 1) +
                            '_q1-3.png', img.astype(np.uint8))
        self.P33 = P33

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()
        # self.P3.Solve()
        self.P3ALTER.Solve()


class Q2():
    def __init__(self):
        self.images = List[MatLike]
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
    q1.P33.Solve()
    # q2 = Q2()
    # q1.Solve()
    # q2.Solve()
    print('Done')
