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


class Q:
    def __init__(self):
        self.images = []
        for i in range(1, 5):
            self.images.append(cv2.imread('./images/img' + str(i) + '.png'))

            width, height, _ = self.images[i - 1].shape
            hist = [0] * 256
            for row in range(width):
                for col in range(height):
                    self.images[i - 1][row][col] = [0.299 * self.images[i - 1][row][col][2] + 0.587 *
                                                    self.images[i - 1][row][col][1] + 0.114 * self.images[i - 1][row][col][0]] * 3
                    hist[int(self.images[i - 1][row][col][0])] += 1
            left_id = 0
            h_id = 0
            for j in range(256):
                if hist[j] != 0 and left_id == 0:
                    left_id = j
                if hist[j] > hist[h_id]:
                    h_id = j
            thresh = 0
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
                plt.savefig('./debug/img' + str(i) + '_histogram.png')
                plt.close()
            except ImportError:
                print('Matplotlib not found, skipping histogram plot')
            for row in range(width):
                for col in range(height):
                    if self.images[i - 1][row][col][0] > thresh:
                        self.images[i - 1][row][col] = [255] * 3
                    else:
                        self.images[i - 1][row][col] = [0] * 3
            cv2.imwrite('./debug/img' + str(i) +
                        '_binary.png', self.images[i - 1])

        @problem
        def P1():
            imgs = deepcopy(self.images)
            for i in range(4):
                width, height, _ = imgs[i].shape
                # 4 connected way
                p = int(0)
                groups = defaultdict(int)

                def find(x):
                    if groups[x] == x:
                        return x
                    else:
                        groups[x] = find(groups[x])
                        return groups[x]

                def union(x, y):
                    groups[find(x)] = find(y)
                compMap = np.zeros((width, height))

                for row in range(width):
                    for col in range(height):
                        if imgs[i][row][col][0] == 255:
                            continue

                        u = find(compMap[row - 1][col])
                        l = find(compMap[row][col - 1])
                        if row == 0:
                            u = 0
                        if col == 0:
                            l = 0
                        if u == 0 and l == 0:
                            p += 1
                            compMap[row][col] = p
                            groups[p] = p
                        elif u == 0:
                            compMap[row][col] = l
                        elif l == 0:
                            compMap[row][col] = u
                        else:
                            compMap[row][col] = l
                            if u != l:
                                union(u, l)
                s = set()
                for w in range(1, p + 1):
                    s.add(find(w))
                total = len(s)
                print('Total objects:', total)
                np.random.seed(0)
                colors = {}
                for c in s:
                    colors[c] = [np.random.randint(0, 256) for _ in range(3)]

                for row in range(width):
                    for col in range(height):
                        if imgs[i][row][col][0] == 255:
                            continue
                        imgs[i][row][col] = colors[int(
                            find(compMap[row][col]))]
                cv2.imwrite('./results/img' + str(i+1) + '_4.png', imgs[i])
        self.P1 = P1

        @problem
        def P2():
            # 8 connected way
            imgs = deepcopy(self.images)
            for i in range(4):
                width, height, _ = imgs[i].shape
                p = -1
                groups = defaultdict(int)

                def find(x):
                    if groups[x] == x:
                        return x
                    else:
                        groups[x] = find(groups[x])
                        return groups[x]

                def union(x, y):
                    groups[find(x)] = find(y)
                compMap = np.zeros((width, height))

                for row in range(width):
                    for col in range(height):
                        if imgs[i][row][col][0] == 255:
                            continue

                        u = ul = ur = l = 0
                        if row > 0:
                            u = find(compMap[row - 1][col])
                        if row > 0 and col > 0:
                            ul = find(compMap[row - 1][col - 1])
                        if row > 0 and col < height - 1:
                            ur = find(compMap[row - 1][col + 1])
                        if col > 0:
                            l = find(compMap[row][col - 1])
                        if u == 0 and l == 0 and ul == 0 and ur == 0:
                            p += 1
                            compMap[row][col] = p
                            groups[p] = p
                        elif u == 0 and ul == 0 and ur == 0:
                            compMap[row][col] = l
                        elif l == 0 and ul == 0 and ur == 0:
                            compMap[row][col] = u
                        elif u == 0 and l == 0 and ur == 0:
                            compMap[row][col] = ul
                        elif u == 0 and l == 0 and ul == 0:
                            compMap[row][col] = ur
                        elif l == 0 and u == 0:
                            compMap[row][col] = ul
                            union(ul, ur)
                        elif l == 0 and ul == 0:
                            compMap[row][col] = u
                        elif l == 0 and ur == 0:
                            compMap[row][col] = u
                        elif u == 0 and ul == 0:
                            compMap[row][col] = l
                            union(l, ur)
                        elif u == 0 and ur == 0:
                            compMap[row][col] = l
                        elif ul == 0 and ur == 0:
                            compMap[row][col] = l
                            union(l, u)
                        elif u == 0:
                            compMap[row][col] = l
                            union(l, ur)
                        elif l == 0:
                            compMap[row][col] = u
                        elif ul == 0:
                            compMap[row][col] = ur
                        elif ur == 0:
                            compMap[row][col] = ul
                        else:
                            compMap[row][col] = l

                s = set()
                for w in range(p + 1):
                    s.add(find(w))
                total = len(s)
                print('Total objects:', total)
                np.random.seed(0)
                colors = {}
                for c in s:
                    colors[c] = [np.random.randint(0, 256) for _ in range(3)]
                for row in range(width):
                    for col in range(height):
                        if imgs[i][row][col][0] == 255:
                            continue
                        imgs[i][row][col] = colors[int(
                            find(compMap[row][col]))]
                cv2.imwrite('./results/img' + str(i+1) + '_8.png', imgs[i])
        self.P2 = P2

    def Solve(self):
        self.P1.Solve()
        self.P2.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
