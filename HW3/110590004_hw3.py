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
        self.images = []
        for i in range(1, 5):
            self.images.append(cv2.imread('./images/img' + str(i) + '.png'))

            thresh = 0
            width, height, _ = self.images[i - 1].shape
            hist = [0] * 256
            print('Grayscaling img' + str(i) + '...')
            with alive_bar(width * height) as bar:
                for row in range(width):
                    for col in range(height):
                        self.images[i - 1][row][col] = [0.299 * self.images[i - 1][row][col][2] + 0.587 *
                                                        self.images[i - 1][row][col][1] + 0.114 * self.images[i - 1][row][col][0]] * 3
                        hist[int(self.images[i - 1][row][col][0])] += 1
                        bar()
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
                        if self.images[i - 1][row][col][0] > thresh:
                            self.images[i - 1][row][col] = [255] * 3
                        else:
                            self.images[i - 1][row][col] = [0] * 3
                        bar()
                import os
                if not os.path.exists('./debug'):
                    os.makedirs('./debug')
                cv2.imwrite('./debug/img' + str(i) +
                            '_binary.png', self.images[i - 1])

        @problem
        def P1():
            imgs = deepcopy(self.images) 
        self.P1 = P1

        @problem
        def P2():
            imgs = deepcopy(self.images)
        self.P2 = P2

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
