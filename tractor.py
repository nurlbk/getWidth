import json

from numpy import mean
from functions import *


class Tractor:
    def __init__(self, url):
        self.coordinates = []
        self.line_limit = 0

        self.getCoordinates(url)
        self.setLineLimit()

    def getCoordinates(self, url):
        with open(url) as f:
            fjson = json.load(f)
        data = fjson['features']

        for i in range(len(data) - 1):
            if data[i]['geometry']['coordinates'][0] == data[i + 1]['geometry']['coordinates'][0] and \
                    data[i]['geometry']['coordinates'][1] == data[i + 1]['geometry']['coordinates'][1]:
                i -= 1
                pass
            else:
                self.coordinates.append(
                    data[i]['geometry']['coordinates'])

        self.coordinates.append(data[len(data) - 1]['geometry']['coordinates'])

    def setLineLimit(self):
        array_of_distances = []

        for i in range(len(self.coordinates) - 1):
            array_of_distances.append(findDistance3857(self.coordinates[i], self.coordinates[i + 1]))

        array_of_distances.sort()
        # print("Mean on Distances:", mean(array_of_distances))
        self.line_limit = array_of_distances[int(len(array_of_distances) / 2.5)] * 1.15

        # Тут мы берем 1/3 от длин и +15%
        # print("Line limit:", self.line_limit)

        # data = pd.DataFrame(array_of_distances)
        # a = int(2 * array_of_distances[len(array_of_distances) - 1])
        # data.hist(bins=a)
        # # plt.plot(data)
        # plt.show()

    def getMiddlePoint(self, i, point1, point2):
        x_diff = point1[0] - point2[0]
        y_diff = point1[1] - point2[1]
        hypotenuse1 = math.sqrt(pow(x_diff, 2) + pow(y_diff, 2))

        if hypotenuse1 > self.line_limit:
            newMiddlePoint = [x_diff / 2 + point2[0], y_diff / 2 + point2[1]]
            self.coordinates.insert(i + 1, newMiddlePoint)
            return self.getMiddlePoint(i, point1, [x_diff / 2 + point2[0], y_diff / 2 + point2[1]])

    def addMiddlePoints(self):
        i = 0
        while i < len(self.coordinates) - 1:
            self.getMiddlePoint(i, self.coordinates[i], self.coordinates[i + 1])
            i += 1
