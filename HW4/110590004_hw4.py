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
        self.labels = [
            ["a349a4", "00a2e8", "fff200", "b97a57"], ["ff7f27", "fff200", "22b14c", "00a2e8", "3f48cc", "a349a4",
                                                       "b97a57", "ffaec9", "ffc90e", "efe4b0", "b5e61d", "99d9ea", "880015"], ["a349a4", "3f48cc", "ed1c24"]
        ]
        for i in range(1, 4):
            img = np.zeros((self.origin_images[i - 1].shape[0], self.origin_images[i - 1].shape[1], 3))
            for row in range(self.origin_images[i - 1].shape[0]):
                for col in range(self.origin_images[i - 1].shape[1]):
                    img[row][col] = self.origin_images[i - 1][row][col]
            self.images.append(img)
        @problem
        def P1():
            class PriorityQueue:
                def __init__(self):
                    self.elements = []

                def empty(self):
                    return len(self.elements) == 0

                def push(self, item, priority):
                    heappush(self.elements, (priority, item))

                def pop(self):
                    return heappop(self.elements)[1]
                def size(self):
                    return len(self.elements)
            def water_shed(image, id):
                seeds = []
                pq = PriorityQueue()
                width, height, _ = image.shape
                land = np.zeros((width, height))
                labeled_image = cv2.imread("./images/img" + str(id) + "_q1-1.png")
                mapping = {}
                label_map = {} 
                for i, l in enumerate(self.labels[id - 1]):
                    # rgb string to bgr tuple
                    rgb = int(l, 16)
                    bgr = (rgb & 0xff, (rgb >> 8) & 0xff, (rgb >> 16) & 0xff)
                    mapping[bgr] = i + 1
                    label_map[i + 1] = bgr
                for row in range(width):
                    for col in range(height):
                        if(labeled_image[row][col][0], labeled_image[row][col][1], labeled_image[row][col][2]) in mapping:
                            land[row][col] = mapping[(labeled_image[row][col][0], labeled_image[row][col][1], labeled_image[row][col][2])]
                            seeds.append((row, col))
                            # mapping.pop((labeled_image[row][col][0], labeled_image[row][col][1], labeled_image[row][col][2]))
                def get_8_neighbors(img, x, y):
                    neighbors = []
                    if x > 0:
                        neighbors.append((x - 1, y))
                        if y > 0:
                            neighbors.append((x - 1, y - 1))
                        if y < img.shape[1] - 1:
                            neighbors.append((x - 1, y + 1))
                    if x < img.shape[0] - 1:
                        neighbors.append((x + 1, y))
                        if y > 0:
                            neighbors.append((x + 1, y - 1))
                        if y < img.shape[1] - 1:
                            neighbors.append((x + 1, y + 1))
                    if y > 0:
                        neighbors.append((x, y - 1))
                    if y < img.shape[1] - 1:
                        neighbors.append((x, y + 1))
                    return np.array(neighbors)
                def distance(c1, c2):
                    return np.sqrt(np.sum((c1 - c2) ** 2))
                def priority(x, y, image):
                    neighbors = get_8_neighbors(image, x, y)
                    colors = [image[n[0]][n[1]] for n in neighbors] + [image[x][y]]
                    return distance(np.max(colors, axis=0), np.min(colors, axis=0))
                for seed in seeds:
                    pq.push(seed, priority(seed[0], seed[1], image))
                def get_neighbors(img, x, y):
                    neighbors = []
                    if x > 0:
                        neighbors.append((x - 1, y))
                    if x < img.shape[0] - 1:
                        neighbors.append((x + 1, y))
                    if y > 0:
                        neighbors.append((x, y - 1))
                    if y < img.shape[1] - 1:
                        neighbors.append((x, y + 1))
                    return np.array(neighbors)
                cn = 0
                arc = []
                while not pq.empty():
                    cn += 1
                    x, y = pq.pop()
                    neighbors = get_neighbors(land, x, y) 
                    if cn %1000 ==0 :
                        arc.append(deepcopy(land))
                    neighbors = np.array([n for n in neighbors if land[n[0]][n[1]] >= 0])
                    if land[x, y] == -2:
                        # if there are different labels in the neighbors, then the pixel is a boundary
                        if np.unique([land[n[0]][n[1]] for n in neighbors if land[n[0]][n[1]] > 0]).size > 1 or neighbors.size == 0: 
                            land[x][y] = -1
                            continue
                        else:
                            land[x][y] = np.max([land[n[0]][n[1]] for n in neighbors])
                    for n in neighbors:
                        if land[n[0]][n[1]] == 0:
                            land[n[0]][n[1]] = -2
                            pq.push((n[0], n[1]), priority(n[0], n[1], image))
                        
                return land, label_map, arc
            for i in range(1, 4):
                land, lm, arc = water_shed(self.images[i - 1], i)
                origin = deepcopy(self.origin_images[i - 1])
                width, height, _ = origin.shape
                # make a mp4 of the process
                frames = []
                for a in arc:
                    frame = deepcopy(origin)
                    for row in range(width):
                        for col in range(height):
                            if a[row][col] == -1:
                                frame[row][col] = [0, 0, 0]
                            elif a[row][col] > 0:
                                frame[row][col] = lm[a[row][col]]
                    frames.append(frame)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter("./images/img" + str(i) + "_q1-3.mp4", fourcc, 10, (height, width)) 
                for frame in frames:
                    out.write(frame)
                out.release()

                # color regions
                for row in range(width):
                    for col in range(height):
                        if land[row][col] <= 0:
                            origin[row][col] = [0, 0, 0]
                        else:
                            origin[row][col] = lm[land[row][col]]
                cv2.imwrite("./images/img" + str(i) + "_q1-2.png", origin)
                print("img" + str(i) + " done")

        self.P1 = P1

    def Solve(self):
        self.P1.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
