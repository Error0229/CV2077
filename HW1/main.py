import cv2
from collections import defaultdict
from copy import deepcopy
import numpy as np
from alive_progress import alive_bar


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
        def P3A():
            MAX_COLORS = 16
            THRESH = 50
            DIVS = 4
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
                colorPool = sorted(
                    colorPool, key=lambda x: len(x[1]), reverse=True)
                for color in colorPool:
                    color[1] = [colorPair[0]
                                for colorPair in sorted(color[1].items(),
                                                        key=lambda x: x[1], reverse=True)[:MAX_COLORS]]
                colors = []
                poolID = 0
                while len(colors) < MAX_COLORS:
                    try:
                        colors.append(colorPool[poolID][1][0])
                    except:
                        poolID = (poolID + 1) % len(colorPool)
                    colorPool[poolID][1].pop(0)
                    poolID = (poolID + 1) % len(colorPool)
                print(f"color platte: {[hex(color) for color in colors]}")
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
        self.P3A = P3A

        @problem
        def P3():
            MAX_COLORS = 16
            THRESH = 50

            def dis(c1, c2):
                return np.linalg.norm(c1 - c2)

            class group:
                def __init__(self, represent=np.ndarray(3, dtype=np.uint8)):
                    self.colors = [represent]
                    self.represent = represent

                def add(self, color):
                    self.colors.append(color)
                    self.represent = self.represent + \
                        (color - self.represent) / len(self.colors)

                def sort(self):
                    self.colors = sorted(
                        self.colors, key=lambda x: dis(x, self.represent))
                    self.represent = self.colors[0]

            imgs = [img.astype(np.float32) for img in self.images]
            for mid, img in enumerate(imgs):
                pool = []
                width, height, _ = img.shape
                AllTheColors = []
                for i in range(width):
                    for j in range(height):
                        AllTheColors.append(img[i, j])
                AllTheColors = np.array(AllTheColors)
                # shuffle the colors
                np.random.seed(125)
                np.random.shuffle(AllTheColors)
                with alive_bar(width*height, spinner='pulse') as bar:
                    for pixel in AllTheColors:
                        id = -1
                        min_dis = float('inf')

                        for pid, color in enumerate(pool):
                            dist = dis(color.represent, pixel)
                            if dist < min_dis:
                                id = pid
                                min_dis = dist
                        if (len(pool) < MAX_COLORS and min_dis > THRESH):
                            pool.append(group(pixel))
                            THRESH = THRESH ** (1/1.01)
                        else:
                            pool[id].add(pixel)
                        bar.text('Processing pixels ')
                        bar()
                for color in pool:
                    color.sort()
                    print(color.represent)

                with alive_bar(width*height, spinner='pulse') as bar:
                    for i in range(width):
                        for j in range(height):
                            pixel = img[i, j]
                            min_dis = float('inf')
                            index = -1
                            for k in range(len(pool)):
                                dist = dis(pool[k].represent, pixel)
                                if dist < min_dis:
                                    min_dis = dist
                                    index = k
                            img[i, j] = pool[index].represent
                            bar()
                            bar.text('Drawing pixel at ' +
                                     str(i) + ' ' + str(j))
                cv2.imwrite('./results/img' + str(mid + 1) +
                            '_q1-3.png', img.astype(np.uint8))
        self.P3 = P3

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()
        self.P3.Solve()
        # self.P3A.Solve()


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
                def BilinearInterpolation(img, scale):
                    result = np.zeros(
                        (int(img.shape[0]*scale), int(img.shape[1]*scale), 3), dtype=np.float32)
                    for row in range(result.shape[0]):
                        for col in range(result.shape[1]):
                            origin_x = (row + 0.5) / scale - 0.5
                            origin_y = (col + 0.5) / scale - 0.5
                            x = int(origin_x)
                            y = int(origin_y)
                            dx = origin_x - x
                            dy = origin_y - y
                            x = max(0, min(x, img.shape[0] - 2))
                            y = max(0, min(y, img.shape[1] - 2))
                            dx = 1 if x >= img.shape[0] - 2 else 0
                            dy = 1 if y >= img.shape[1] - 2 else 0
                            result[row, col] = (1-dx)*(1-dy)*img[x, y] + dx*(1-dy)*img[x+1, y] + \
                                (1-dx)*dy*img[x, y+1] + dx*dy*img[x+1, y+1]
                    return result
                result = BilinearInterpolation(imgs[i], 2)
                cv2.imwrite('./results/img' + str(i + 1) +
                            '_q2-2-double.png', result.astype(np.uint8))

                result = BilinearInterpolation(imgs[i], 0.5)
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
