from scipy.stats import mode
from tractor import *
from lattice import *
import pandas as pd
import matplotlib.pyplot as plt


def arrayLimit(array_of_widths):
    distanceMode = mode(array_of_widths)
    # print(distanceMode)
    while array_of_widths[len(array_of_widths) - 1] > 2 * int(distanceMode[0]):
        array_of_widths.pop()

    return array_of_widths


class getWidth(Tractor):
    def __init__(self, url, count_type):
        super().__init__(url)
        self.tractor_width = 0
        self.iterator = 0
        self.lattice = lattice()
        self.count_type = count_type

        self.addMiddlePoints()
        self.create_grid()
        self.probably_width = self.createHist()

    def getProbablyWidth(self):
        return round(self.probably_width, 1)

    # https://www.youtube.com/watch?v=Qgevy75co8c
    # num.py
    def create_grid(self):
        borders = cellBorders(self.coordinates)
        grid_size = self.line_limit
        self.lattice.set_grid([borders[0], borders[1]], [borders[2], borders[3]],
                              grid_size)

    def getWidth(self, count_type):
        i = 0
        widths = []
        if count_type == 1:
            # можно добавить for так как кол-во точек не меняется
            for i in range(len(self.coordinates) - 1):

                # ограничение по рамке
                # if 30 > parsedGridPoint[0] or parsedGridPoint[0] > 120 or \
                #         30 > parsedGridPoint[1] or parsedGridPoint[1] > 180:
                #
                #     self.lattice.get_grid(parsedGridPoint).append(i)

                near_Points = []
                min_height = 100

                # определяем индексы сетки для выбранной точки
                parsedGridPoint = getCell(self.coordinates[i],
                                          self.lattice.get_min_point(),
                                          self.lattice.get_cell_size())

                for y in range(3):
                    for z in range(3):
                        for l in range(
                                len(self.lattice.get_grid([parsedGridPoint[0] - 1 + y,
                                                           parsedGridPoint[1] - 1 + z]))):
                            comparative_Point_id = \
                                self.lattice.get_grid([parsedGridPoint[0] - 1 + y,
                                                       parsedGridPoint[1] - 1 + z])[l]
                            near_Points.append(comparative_Point_id)
                near_Points.sort()

                for j in range(len(near_Points)):
                    if near_Points[j] - near_Points[j - 1] == 1:
                        if abs(getDirection(self.coordinates[i - 1],
                                            self.coordinates[i + 1]) -
                               getDirection(self.coordinates[near_Points[j]],
                                            self.coordinates[near_Points[j] - 1])) < 5:  # угол

                            # ТУТ ПРО СИСТЕМУ КООРДИНАТ
                            probably_height = getHeight4326_2(self.coordinates[i],
                                                              self.coordinates[near_Points[j] - 1],
                                                              self.coordinates[near_Points[j]])
                            if min_height > probably_height:
                                min_height = probably_height

                if min_height != 100:
                    widths.append(round(min_height, 1))
                    # widths.append(round(2 * round(min_height, 1)) / 2)

                self.lattice.get_grid(parsedGridPoint).append(i)

        elif count_type == 2:
            while i < len(self.coordinates) - 2:
                # ограничение по рамке
                # if 30 > parsedGridPoint[0] or parsedGridPoint[0] > 120 or \
                #         30 > parsedGridPoint[1] or parsedGridPoint[1] > 180:
                #
                #     self.lattice.get_grid(parsedGridPoint).append(i)
                #

                near_Points = []
                min_height = 100

                # определяем индексы сетки для выбранной точки
                parsedGridPoint = getCell([(self.coordinates[i][0] + self.coordinates[i + 1][0]) / 2,
                                           (self.coordinates[i][1] + self.coordinates[i + 1][1]) / 2],
                                          self.lattice.get_min_point(), self.lattice.get_cell_size())

                distance_grid = [abs(int((self.coordinates[i][0] - self.coordinates[i + 1][0]) / (2 * self.line_limit))) + 1,
                                 abs(int((self.coordinates[i][1] - self.coordinates[i + 1][1]) / (2 * self.line_limit))) + 1]

                for y in range(2 * distance_grid[0] + 1):
                    for z in range(2 * distance_grid[1] + 1):

                        for l in range(
                                len(self.lattice.get_grid([parsedGridPoint[0] - distance_grid[0] + y,
                                                           parsedGridPoint[1] - distance_grid[1] + z]))):

                            comparative_Point_id = \
                                self.lattice.get_grid([parsedGridPoint[0] - distance_grid[0] + y,
                                                       parsedGridPoint[1] - distance_grid[1] + z])[l]
                            near_Points.append(comparative_Point_id)

                near_Points.sort()

                for j in range(len(near_Points)):
                    if abs(getDirection(self.coordinates[i], self.coordinates[i + 1]) -
                           getDirection(self.coordinates[j - 1], self.coordinates[j + 1])) < 5:  # угол

                        # ТУТ ПРО СИСТЕМУ КООРДИНАТ
                        probably_height = getHeight4326_2(self.coordinates[j],
                                                          self.coordinates[i],
                                                          self.coordinates[i + 1])
                        self.iterator += 1

                        if min_height > probably_height:
                            min_height = probably_height

                if min_height != 100:
                    widths.append(round(min_height, 1))

                self.lattice.get_grid(parsedGridPoint).append(i)
                i += 1

        elif count_type == 3:
            for i in range(len(self.coordinates) - 1):
                # ограничение по рамке
                # if 30 > parsedGridPoint[0] or parsedGridPoint[0] > 120 or \
                #         30 > parsedGridPoint[1] or parsedGridPoint[1] > 180:
                #
                #     self.lattice.get_grid(parsedGridPoint).append(i)
                #

                near_Points = []
                min_height = 100

                # определяем индексы сетки для выбранной точки
                parsedGridPoint = getCell([(self.coordinates[i][0] + self.coordinates[i + 1][0]) / 2,
                                           (self.coordinates[i][1] + self.coordinates[i + 1][1]) / 2],
                                          self.lattice.get_min_point(),
                                          self.lattice.get_cell_size())

                for y in range(3):
                    for z in range(3):
                        for l in range(
                                len(self.lattice.get_grid([parsedGridPoint[0] - 1 + y,
                                                           parsedGridPoint[1] - 1 + z]))):
                            comparative_Point_id = \
                                self.lattice.get_grid([parsedGridPoint[0] - 1 + y,
                                                       parsedGridPoint[1] - 1 + z])[l]
                            near_Points.append(comparative_Point_id)
                near_Points.sort()

                for j in range(len(near_Points)):
                    if abs(getDirection(self.coordinates[i],
                                        self.coordinates[i + 1]) -
                           getDirection(self.coordinates[near_Points[j] + 1],
                                        self.coordinates[near_Points[j] - 1])) < 5:  # угол

                        # ТУТ ПРО СИСТЕМУ КООРДИНАТ
                        probably_height = getHeight4326_2(self.coordinates[near_Points[j]],
                                                          self.coordinates[i],
                                                          self.coordinates[i + 1])
                        self.iterator += 1
                        if min_height > probably_height:
                            min_height = probably_height

                if min_height != 100:
                    widths.append(round(min_height, 1))
                    # widths.append(round(2 * round(min_height, 1)) / 2)

                self.lattice.get_grid(parsedGridPoint).append(i)
                i += 1

        widths.sort()
        # Мод равен ширине
        return widths

    def createHist(self):
        array_of_widths = self.getWidth(self.count_type)
        # array_of_widths = arrayLimit(array_of_widths)

        data = pd.DataFrame(array_of_widths)
        a = int(2 * array_of_widths[len(array_of_widths) - 1])

        data.hist(bins=a)
        # plt.plot(data)
        plt.show()
        # print(data.describe())
        # print("Number of operations:", self.iterator)

        return float(mean(array_of_widths))

