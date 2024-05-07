import cv2
import hashlib
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
                                                       "b97a57", "ffaec9", "ffc90e", "efe4b0", "b5e61d", "99d9ea", "880015","c8bfe7", "ed1c24"], ["a349a4", "3f48cc", "ed1c24"]
        ]
        VIDEO = True
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
                # grayscale
                # let he last dimension become 1d
                rs = np.zeros((image.shape[0], image.shape[1], 1))
                for row in range(image.shape[0]):
                    for col in range(image.shape[1]):
                        rs[row][col] = 0.299 * image[row][col][2] + 0.587 * image[row][col][1] + 0.114 * image[row][col][0]
                image = deepcopy(rs)
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
                group_mean = {}
                for row in range(width):
                    for col in range(height):
                        if(labeled_image[row][col][0], labeled_image[row][col][1], labeled_image[row][col][2]) in mapping:
                            land[row][col] = mapping[(labeled_image[row][col][0], labeled_image[row][col][1], labeled_image[row][col][2])]
                            seeds.append((row, col))
                            mean, cnt= group_mean.get(land[row][col], (np.zeros(3), 0))
                            group_mean[land[row][col]] = (cnt * mean + image[row][col]) / (cnt + 1), cnt + 1
                def legal(x, y, w, h):
                    return x >= 0 and y >= 0 and x < w and y < h
                def get_n_neighbors(img, x, y, n = 1):
                    neighbors = []
                    width, height, _ = img.shape
                    for i in range(-n, n+1):
                        for j in range(-n, n+1):
                            if legal(x + i, y + j, width, height):
                                neighbors.append((x + i, y + j))
                    return np.array(neighbors)
                # cache = {} 
                # MAX_CACHE_SIZE = 100
                def distance(c1, c2):
                    return np.sqrt(np.sum((c1 - c2) ** 2))
                    # key = hash_colors(c1, c2)
                    # if key in cache:
                    #     return cache[key]
                    # d = np.sqrt(np.sum((c1 - c2) ** 2))
                    # cache[key] = d
                    # key1, key2 = tuple(sorted((c1.tobytes(), c2.tobytes())))
                    # if key1 in cache or key2 in cache:
                    #     return cache[key1]
                    # d = np.sqrt(np.sum((c1 - c2) ** 2))
                    # cache[key1] = d
                    # cache[key2] = d
                    # if len(cache) > MAX_CACHE_SIZE: 
                    #     # Evict least recently used item
                    #     cache.pop(next(iter(cache)))
                    # return d

                # def hash_colors(c1, c2):
                #     hash_input = tuple(sorted((c1.tobytes(), c2.tobytes())))
                #     return hashlib.sha1(str(hash_input).encode()).hexdigest() 
                # def priority(x, y, image, group):
                #     neighbors = get_n_neighbors(image, x, y, 1)
                #     colors = [image[n[0]][n[1]] for n in neighbors] + [image[x][y]]
                #     # return distance(np.mean(colors, axis=0), image[x][y])
                #     # return np.mean([distance(c, image[x][y]) for c in colors]) + 0.1 * np.std([distance(c, image[x][y]) for c in colors]) 
                #     clrs = np.array([distance(c, image[x][y]) for c in colors]) 
                #     # print(np.std(clrs), np.mean(clrs), distance(group, image[x][y]))
                #     # return distance(group, image[x][y])+  np.std(clrs) + np.mean(clrs)
                #     return 0.042*np.std(clrs) + 0.69*np.mean(clrs) + 0.1 * distance(group, image[x][y]) 
                #     # return np.max([distance(c, image[x][y]) for c in colors])
                def sobel(x, y, image):
                    sobelX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
                    sobelY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
                    k = np.zeros((3, 3))
                    for i in range(3):
                        for j in range(3):
                            if legal(x + i - 1, y + j - 1, width, height):
                                k[i][j] = image[x + i - 1][y + j - 1][0]
                    gx = np.sum(sobelX * k)
                    gy = np.sum(sobelY * k)
                    return np.sqrt(gx ** 2 + gy ** 2)
                def priority(x, y, image, group_mean_color):
                    neighbors = get_n_neighbors(image, x, y, 1)
                    colors = [image[n[0], n[1]] for n in neighbors]  # Only consider labeled neighbors

                    
                    colors = np.array(colors)
                    mean_color = np.mean(colors, axis=0)  # Compute mean color of the neighbors
                    color_variance = np.var(colors, axis=0).sum()  # Sum of variances of RGB channels
                    
                    color_distance = distance(image[x, y], mean_color)
                    group_distance = distance(image[x, y], group_mean_color)

                    
                    # Adjust weights for each component based on your image specifics and desired segmentation sharpness
                    # priority_value = 0.5 * color_distance + 0.5 * color_variance + 0.1 * group_distance + 0.1 * sobel(x, y, image)
                    priority_value = sobel(x, y, image) + 0.5 * color_distance + 0.5 * color_variance 
                    return priority_value
 
                    
                for seed in seeds:
                    pq.push(seed, priority(seed[0], seed[1], image, group_mean[land[seed[0]][seed[1]]][0]))
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
                print(f"flooding image {id}")
                with alive_bar(width * height) as bar:

                    while not pq.empty():
                        cn += 1
                        x, y = pq.pop()
                        neighbors = get_neighbors(land, x, y) 
                        if VIDEO and cn % 10000 ==0 :
                            arc.append(deepcopy(land))
                        neighbors = np.array([n for n in neighbors if land[n[0]][n[1]] >= 0])
                        if land[x, y] == -2:
                            # if there are different labels in the neighbors, then the pixel is a boundary
                            if np.unique([land[n[0]][n[1]] for n in neighbors if land[n[0]][n[1]] > 0]).size > 1 or neighbors.size == 0: 
                                land[x][y] = -1
                                bar()
                                continue
                            else:
                                land[x][y] = np.max([land[n[0]][n[1]] for n in neighbors])
                                mean, cnt = group_mean.get(land[x][y], (np.zeros(3), 0))
                                group_mean[land[x][y]] = (cnt * mean + image[x][y]) / (cnt + 1), cnt + 1
                        for n in neighbors:
                            if land[n[0]][n[1]] == 0:
                                land[n[0]][n[1]] = -2
                                pq.push((n[0], n[1]), priority(n[0], n[1], image, group_mean[land[x][y]][0]) )
                            
                        bar()
                return land, label_map, arc

            for i in range(1, 4):
                land, lm, arc = water_shed(self.images[i - 1], i)
                origin = deepcopy(self.origin_images[i - 1])
                width, height, _ = origin.shape
                # make a mp4 of the process
                if VIDEO:
                    frames = []
                    print("masking video")
                    with alive_bar(len(arc)) as bar:
                        for a in arc:
                            frame = deepcopy(origin)
                            for row in range(width):
                                for col in range(height):
                                    if a[row][col] == -1:
                                        frame[row][col] = [0, 0, 0]
                                    elif a[row][col] > 0:
                                        frame[row][col] = (frame[row][col] * 0.3 + np.array(lm[a[row][col]]) * 0.7).astype(np.uint8)
                            frames.append(frame)
                            bar()
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter("./images/img" + str(i) + "_q1-3.mp4", fourcc, 3, (height, width)) 
                    print("writing video")
                    for frame in frames:
                        out.write(frame)
                    out.release()

            # color regions
                for row in range(width):
                    for col in range(height):
                        if land[row][col] <= 0:
                            origin[row][col] = [0, 0, 0]
                        else:
                            # origin[row][col] = lm[land[row][col]]
                            # instead of cover the original image, we can tint the region
                            origin[row][col] = (origin[row][col] * 0.3 + np.array(lm[land[row][col]]) * 0.7).astype(np.uint8) 
                cv2.imwrite("./images/img" + str(i) + "_q1-2.png", origin)
                print("img" + str(i) + " done")

        self.P1 = P1

    def Solve(self):
        self.P1.Solve()


if __name__ == '__main__':
    q = Q()
    q.Solve()
    print('Done')
