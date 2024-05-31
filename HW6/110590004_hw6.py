
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
                    r, g, b = self.origin_images[i -
                                                 1][row][col].astype(np.float64)
                    img[row][col] = 0.299 * r + 0.587 * g + 0.114 * b
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

        def gaussian_filter(img, kernel_size, sigma=1):
            kernel = np.zeros((kernel_size, kernel_size))
            offset = kernel_size // 2
            for i in range(0, kernel_size):
                for j in range(0, kernel_size):
                    kernel[i][j] = np.exp(-((i - offset) **
                                          2 + (j - offset)**2) / (2 * sigma**2))
            kernel /= np.sum(kernel)
            h, w = img.shape
            result = np.zeros((h, w))
            with alive_bar(h * w) as bar:
                for row in range(0, h):
                    for col in range(0, w):
                        if row == 0 or row == h - 1 or col == 0 or col == w - 1:
                            result[row][col] = img[row][col]
                        neighbors = get_n_neighbors(img, row, col, kernel_size)
                        result[row][col] = np.sum(neighbors * kernel)
                        bar()
            for i in range(h):
                result[i][0] = result[i][1]
                result[i][w-1] = result[i][w-2]
            for i in range(w):
                result[0][i] = result[1][i]
                result[h-1][i] = result[h-2][i]
            return result

        def Sobel(img):
            kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
            h, w = img.shape
            result_G = np.zeros((h, w))
            result_theta = np.zeros((h, w))
            with alive_bar(h * w) as bar:
                # Skip the border
                for row in range(h):
                    for col in range(w):
                        if row == 0 or row == h - 1 or col == 0 or col == w - 1:
                            result_G[row][col] = 0
                            result_theta[row][col] = 0
                            bar()
                            continue
                        neighbors = get_n_neighbors(img, row, col, 3)
                        Gx = np.sum(neighbors * kernel_x)
                        Gy = np.sum(neighbors * kernel_y)
                        result_G[row][col] = np.sqrt(Gx**2 + Gy**2)
                        result_theta[row][col] = np.arctan2(Gy, Gx)
                        bar()
            return result_G, result_theta

        def non_maximum_suppression(G, theta):
            h, w = G.shape
            result = np.zeros((h, w))
            for row in range(h):
                for col in range(w):
                    rad = theta[row][col]
                    angle = np.rad2deg(rad) % 180
                    neighbors = get_n_neighbors(G, row, col, 3)
                    dirs = [0, 45, 90, 135]
                    closet_dir = min(dirs, key=lambda x: abs(x-angle))
                    if closet_dir == 0:
                        if G[row][col] >= neighbors[1][1] and G[row][col] >= neighbors[1][2]:
                            result[row][col] = G[row][col]
                    elif closet_dir == 45:
                        if G[row][col] >= neighbors[1][1] and G[row][col] >= neighbors[2][2]:
                            result[row][col] = G[row][col]
                    elif closet_dir == 90:
                        if G[row][col] >= neighbors[1][1] and G[row][col] >= neighbors[2][1]:
                            result[row][col] = G[row][col]
                    elif closet_dir == 135:
                        if G[row][col] >= neighbors[1][1] and G[row][col] >= neighbors[2][0]:
                            result[row][col] = G[row][col]
            return result

        def double_thresholding(img, low, high):
            h, w = img.shape
            result = np.zeros((h, w))
            for row in range(h):
                for col in range(w):
                    if img[row][col] >= high:
                        result[row][col] = 255
                    elif img[row][col] >= low:
                        result[row][col] = 128
            return result

        def edge_tracking_by_hysteresis(img):

            h, w = img.shape
            visited = np.zeros((h, w))

            def dfs(q: list):
                while len(q) > 0:
                    r, c = q.pop()
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if legal(h, w, r + i, c + j) and img[r + i][c + j] == 128 and visited[r + i][c + j] == 0:
                                visited[r + i][c + j] = 1
                                img[r + i][c + j] = 255
                                q.append((r + i, c + j))
            for row in range(h):
                for col in range(w):
                    # flood from strong edge
                    if img[row][col] == 255 and visited[row][col] == 0:
                        visited[row][col] = 1
                        dfs([(row, col)])
            # set weak edge to 0
            for row in range(h):
                for col in range(w):
                    if img[row][col] == 128:
                        img[row][col] = 0
            return img

        def save_img(img, name):
            img = img.astype(np.uint8)
            cv2.imwrite(name, img)

        @problem
        def P1():
            for i in range(1, 4):
                print(f'Processing img{i}.jpg')
                print('Gaussian filter')
                gaussian = gaussian_filter(self.images[i - 1], 5, 0.9)
                save_img(gaussian, f'./debug/img{i}_gaussian.jpg')
                print('Processing Sobel operator')
                G, theta = Sobel(gaussian)
                save_img(G, f'./debug/img{i}_G.jpg')
                print('Non-maximum suppression')
                non_max = non_maximum_suppression(G, theta)
                save_img(non_max, f'./debug/img{i}_non_max.jpg')
                print('Double thresholding')
                double_thresh = double_thresholding(non_max, 80, 150)
                save_img(double_thresh, f'./debug/img{i}_double_thresh.jpg')
                print('Edge tracking by hysteresis')
                edge_tracking = edge_tracking_by_hysteresis(
                    deepcopy(double_thresh))
                save_img(edge_tracking, f'./results/img{i}_sobel.jpg')
        self.P1 = P1

    def Solve(self):
        self.P1.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
