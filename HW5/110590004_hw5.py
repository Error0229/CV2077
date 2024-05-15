import cv2
from copy import deepcopy
import numpy as np
from alive_progress import alive_bar, config_handler
from heapq import *

config_handler.set_global(spinner='crab', bar='smooth')


class Problem:
    def __init__(self, func=None):
        self.Solve = func


def problem(func):
    return Problem(func)


class Q:
    def __init__(self):
        self.origin_images = [cv2.imread(
            './images/img' + str(i) + '.jpg') for i in range(1, 4)]
        self.images = []
        for i in range(1, 4):
            img = np.zeros(
                (self.origin_images[i - 1].shape[0], self.origin_images[i - 1].shape[1]), dtype=np.float64)
            for row in range(self.origin_images[i - 1].shape[0]):
                for col in range(self.origin_images[i - 1].shape[1]):
                    img[row][col] = self.origin_images[i - 1][row][col][0].astype(np.float64)
            self.images.append(img)
        def legal(h, w, row, col):
            return row >= 0 and row < h and col >= 0 and col < w
        def get_n_neighbors(img, row, col, n):
            result = np.zeros((n, n))
            h, w = img.shape
            offset = n // 2
            for i in range(n):
                for j in range(n):
                    if legal(h, w, row + i - offset, col + j - offset):
                        result[i][j] = img[row + i - offset][col + j - offset]
            return result
        def mean_filter(img, kernel_size):
            kernel = np.ones((kernel_size, kernel_size)) / kernel_size**2
            h, w = img.shape
            result = np.zeros((h, w))
            with alive_bar(h * w) as bar:
                for row in range(h):
                    for col in range(w):
                        neighbors = get_n_neighbors(img, row, col, kernel_size)
                        result[row][col] = np.sum(neighbors * kernel)
                        bar()
            return result
        def median_filter(img, kernel_size):
            h, w = img.shape
            with alive_bar(h * w) as bar:
                result = np.zeros((h, w))
                for row in range(h):
                    for col in range(w):
                        neighbors = get_n_neighbors(img, row, col, kernel_size)
                        result[row][col] = np.median(neighbors)
                        bar()
            return result
        def gaussian_filter(img, kernel_size):
            kernel = np.zeros((kernel_size, kernel_size))
            offset = kernel_size // 2
            for i in range(kernel_size):
                for j in range(kernel_size):
                    kernel[i][j] = np.exp(-((i - offset)**2 + (j - offset)**2) / (2 * 1**2))
            kernel /= np.sum(kernel)
            h, w = img.shape
            result = np.zeros((h, w))
            with alive_bar(h * w) as bar:
                for row in range(h):
                    for col in range(w):
                        neighbors = get_n_neighbors(img, row, col, kernel_size)
                        result[row][col] = np.sum(neighbors * kernel)
                        bar()
            return result
        @problem
        def P1():
            for i in range(1, 4):
                print(f'Processing img{i}.jpg')
                mean_3 = mean_filter(self.images[i - 1], 3)
                mean_7 = mean_filter(self.images[i - 1], 7)
                cv2.imwrite(f'./results/img{i}_q1_3.jpg', mean_3)
                cv2.imwrite(f'./results/img{i}_q1_7.jpg', mean_7)
                median_3 = median_filter(self.images[i - 1], 3)
                median_7 = median_filter(self.images[i - 1], 7)
                cv2.imwrite(f'./results/img{i}_q2_3.jpg', median_3)
                cv2.imwrite(f'./results/img{i}_q2_7.jpg', median_7)
                gaussian_3 = gaussian_filter(self.images[i - 1], 3)
                gaussian_7 = gaussian_filter(self.images[i - 1], 7)
                cv2.imwrite(f'./results/img{i}_q3_3.jpg', gaussian_3)
                cv2.imwrite(f'./results/img{i}_q3_7.jpg', gaussian_7)
        self.P1 = P1

    def Solve(self):
        self.P1.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
