import cv2
from collections import defaultdict
from copy import deepcopy
import numpy as np
from alive_progress import alive_bar, config_handler

config_handler.set_global(spinner='crab', bar='smooth')


class Problem:
    def __init__(self, func=None):
        self.Solve = func


def problem(func):
    return Problem(func)


class Q:
    def __init__(self):
        self.origin_images = [cv2.imread(
            './images/img' + str(i) + '.jpg') for i in range(1, 5)]
        # self.origin_images = [cv2.imread('./images/test_32.png')]
        self.images = []
        for i in range(1, self.origin_images.__len__() + 1):
            thresh = 0
            width, height, _ = self.origin_images[i - 1].shape
            hist = [0] * 256
            print('Grayscaling img' + str(i) + '...')
            with alive_bar(width * height) as bar:
                image = np.zeros((width, height))
                for row in range(width):
                    for col in range(height):
                        image[row, col] = 0.299 * self.origin_images[i - 1][row][col][2] + 0.587 * \
                            self.origin_images[i - 1][row][col][1] + \
                            0.114 * self.origin_images[i - 1][row][col][0]
                        hist[int(image[row, col])] += 1
                        bar()
                self.images.append(image)
            # Triangular threshold
            # smooth the histogram
            smooth = 12
            for j in range(256):
                hist[j] = sum(
                    hist[max(0, j - smooth):min(256, j + smooth + 1)]) / (2 * smooth + 1)
            left_id = 0
            h_id = 0
            for j in range(256):
                if hist[j] != 0 and left_id == 0:
                    left_id = j
                if hist[j] > hist[h_id]:
                    h_id = j
            a = (hist[h_id] - hist[left_id]) / (h_id - left_id)
            b = hist[left_id] - a * left_id
            max_val = 0
            for j in range(left_id, h_id + 1):
                if a * j + b - hist[j] > max_val:
                    max_val = a * j + b
                    thresh = j
            try:
                import matplotlib.pyplot as plt
                plt.bar(range(256), hist)
                # draw the line with a and b
                x = np.linspace(0, 255, 256)
                y = a * x + b
                plt.plot(x, y, 'r')
                plt.axvline(x=thresh, color='r')
                plt.title('Histogram')
                plt.xlabel('Intensity')
                plt.ylabel('Frequency')
                # create the folder if not exist
                import os
                if not os.path.exists('./debug'):
                    os.makedirs('./debug')
                plt.savefig('./debug/img' + str(i) + '_histogram.png')
                plt.close()
            except ImportError:
                print('Matplotlib not found, skipping histogram plot')

            print(f'Threshold for img{i}: {thresh}')
            print(f'Thresholding img{i}...')
            with alive_bar(width * height) as bar:
                for row in range(width):
                    for col in range(height):
                        if self.images[i - 1][row][col] > thresh:
                            self.images[i - 1][row][col] = 0
                        else:
                            self.images[i - 1][row][col] = 255
                        bar()
                import os
                if not os.path.exists('./debug'):
                    os.makedirs('./debug')
                cv2.imwrite('./debug/img' + str(i) +
                            '_binary.png', self.images[i - 1])

        def get_neighbors_8(image, i, j, width, height):  # get 8-neighbors
            neighbors = []
            for x in range(-1, 2):
                row = np.zeros(3)
                for y in range(-1, 2):
                    if i + x < 0 or i + x >= width or j + y < 0 or j + y >= height:
                        row[y + 1] = 0
                    else:
                        row[y + 1] = image[i + x][j + y]
                neighbors.append(row)
            return np.array(neighbors)

        def get_neighbors_4(image, i, j, width, height):  # get 4-neighbors
            result = np.zeros((3, 3))
            if i - 1 >= 0:
                result[0, 1] = image[i - 1, j]
            if i + 1 < width:
                result[2, 1] = image[i + 1, j]
            if j - 1 >= 0:
                result[1, 0] = image[i, j - 1]
            if j + 1 < height:
                result[1, 2] = image[i, j + 1]
            return result

        def get_neighbors_corner(image, i, j, width, height):  # get corner neighbors
            result = np.zeros((3, 3))
            if i - 1 >= 0 and j - 1 >= 0:
                result[0, 0] = image[i - 1, j - 1]
            if i - 1 >= 0 and j + 1 < height:
                result[0, 2] = image[i - 1, j + 1]
            if i + 1 < width and j - 1 >= 0:
                result[2, 0] = image[i + 1, j - 1]
            if i + 1 < width and j + 1 < height:
                result[2, 2] = image[i + 1, j + 1]
            return result

        def critical(neighbors):
            if np.sum(neighbors[0, :]) != 0 and np.sum(neighbors[2, :]) != 0 and np.sum(neighbors[1, :]) == 0:
                return True
            if np.sum(neighbors[:, 0]) != 0 and np.sum(neighbors[:, 2]) != 0 and np.sum(neighbors[:, 1]) == 0:
                return True
            # analog corner conditions
            if neighbors[2, 2] != 0 and neighbors[1, 2] == 0 and neighbors[2, 1] == 0 and neighbors[0, 1] != 0 and neighbors[1, 0] != 0:
                return True
            if neighbors[0, 0] != 0 and neighbors[1, 0] == 0 and neighbors[0, 1] == 0 and neighbors[1, 2] != 0 and neighbors[2, 1] != 0:
                return True
            if neighbors[2, 0] != 0 and neighbors[1, 0] == 0 and neighbors[2, 1] == 0 and neighbors[0, 1] != 0 and neighbors[1, 2] != 0:
                return True
            if neighbors[0, 2] != 0 and neighbors[1, 2] == 0 and neighbors[0, 1] == 0 and neighbors[1, 0] != 0 and neighbors[2, 1] != 0:
                return True
            return False

        @problem
        def P1():
            imgs = deepcopy(self.images)
            # 8-distance transform
            print('8-distance transform...')
            for i in range(imgs.__len__()):
                max_h = 0
                width, height = imgs[i].shape
                f0 = np.zeros((width, height))
                for row in range(width):
                    for col in range(height):
                        if imgs[i][row][col] == 0:
                            f0[row][col] = 0
                        else:
                            f0[row][col] = 1
                f_pre = deepcopy(f0)
                fm = np.zeros((width, height))
                local_max = np.zeros((width, height))
                while True:
                    flag = 0
                    local_max = np.zeros((width, height))
                    with alive_bar(width * height) as bar:
                        for row in range(width):
                            for col in range(height):
                                if f0[row][col] == 0:
                                    bar()
                                    continue
                                neighbors = get_neighbors_4(
                                    f_pre, row, col, width, height)
                                fm[row, col] = f0[row, col] + min(
                                    neighbors[0, 1], neighbors[1, 0], neighbors[1, 2], neighbors[2, 1])
                                local_max[row, col] = 1 if fm[row,
                                                              col] >= np.max(neighbors) else 0
                                if fm[row][col] != f_pre[row][col]:
                                    flag = 1
                                bar()
                    f_pre = deepcopy(fm)

                    if flag == 0:
                        break
                temp = np.zeros((width, height, 3))
                for row in range(width):
                    for col in range(height):
                        # print(int(fm[row][col]), end=' ')
                        temp[row][col] = 0 if fm[row][col] == 0 else fm[row][col] * \
                            255 / np.max(fm)
                    # print()
                cv2.imwrite('./results/img' + str(i + 1) + '_q1-1.jpg', temp)

                # boundary_points = set()
                # for row in range(width):
                #     for col in range(height):
                #         if (fm[row][col] != 1):
                #             continue
                #         neighbors = get_neighbors_8(
                #             fm, row, col, width, height)
                #         for x in range(-1, 2):
                #             for y in range(-1, 2):
                #                 if neighbors[x + 1][y + 1] == 0 and (row + x >= 0 and row + x < width and col + y >= 0 and col + y < height):
                #                     boundary_points.add((row + x, col + y))
                # draw boundary points
                # temp = np.zeros((width, height, 3))
                # for point in boundary_points:
                #     temp[point[0], point[1]] = [255, 255, 255]
                # cv2.imwrite('./debug/img' + str(i + 1) + '_boundary.jpg', temp)
                # # print('Boundary points:', boundary_points)
                result = deepcopy(f0)
                print('Skeletonizing...')
                max_h = int(np.max(fm))
                for h in range(1, max_h + 1):
                    with alive_bar(width * height) as bar:
                        for row in range(width):
                            for col in range(height):
                                if (fm[row][col] != h):
                                    bar()
                                    continue
                                # F = find_feature_points((row, col), fm[row][col])
                                # if len(F) >= 8:
                                #     result[row, col] = 1
                                neighbors = get_neighbors_8(
                                    fm, row, col, width, height)
                                # if (max(neighbors[0, 0], neighbors[0, 1], neighbors[1, 0]) < fm[row, col]):
                                #     result[row, col] = 1
                                if (fm[row, col] < np.max(neighbors)):
                                    result[row, col] = 0
                                    if critical(get_neighbors_8(result, row, col, width, height)):
                                        result[row, col] = 1
                                bar()
                # thinning
                k1 = np.array([[0, 0, 0], [-1, 1, -1], [1, 1, 1]])
                k2 = np.array([[-1, 0, 0], [1, 1, 0], [-1, 1, -1]])
                # rotate k1, k2 for 3 times
                SE1 = []
                SE2 = []
                for _ in range(4):
                    SE1.append(k1)
                    SE2.append(k2)
                    k1 = np.rot90(k1)
                    k2 = np.rot90(k2)

                def check_SE(kernel, qd, se):
                    se1 = se[qd]
                    for x in range(3):
                        for y in range(3):
                            if se1[x][y] == -1:
                                continue
                            if kernel[x][y] != se1[x][y]:
                                return False
                    return True

                for  _ in range(2):
                    for q in range(4):
                        for row in range(width):
                            for col in range(height):
                                if result[row][col] == 0:
                                    continue
                                if check_SE(get_neighbors_8(result, row, col, width, height), q, SE1):
                                    result[row][col] = 0
                        for row in range(width):
                            for col in range(height):
                                if result[row][col] == 0:
                                    continue
                                if check_SE(get_neighbors_8(result, row, col, width, height), q, SE2):
                                    result[row][col] = 0
                for row in range(width):
                    for col in range(height):
                        result[row][col] = 0 if result[row][col] == 0 else 255

                cv2.imwrite('./results/img' + str(i + 1) + '_q1-2.jpg', result)
        self.P1 = P1

        @problem
        def P2():
            imgs = deepcopy(self.origin_images)
        self.P2 = P2

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
