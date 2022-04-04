import math

import pyproj
from shapely.ops import transform as shapelyTransform
from shapely.geometry import Point
from geopy.distance import geodesic
from geopy.distance import great_circle

wgs84 = pyproj.CRS('EPSG:3857')
utm = pyproj.CRS('EPSG:4326')
project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform


def convertPoint(point):
    utm_point = shapelyTransform(project, Point(point))
    converted_point = [utm_point.y, utm_point.x]
    return converted_point


def findDistance4326geodesic(point1, point2):
    return geodesic(point1, point2).m


def findDistance4326great_circle(point1, point2):
    return great_circle(point1, point2).m


def findDistance3857(point1, point2):
    return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))


def getHeight3857(point1, point2, point3):
    hypotenuse1 = findDistance3857(point1, point2)
    hypotenuse2 = findDistance3857(point1, point3)
    hypotenuse3 = findDistance3857(point2, point3)
    p = (hypotenuse1 + hypotenuse2 + hypotenuse3) / 2
    return round(2 * math.sqrt(p * (p - hypotenuse1) * (p - hypotenuse2) * (p - hypotenuse3)) / hypotenuse3, 1)


def getHeight4326(point1, point2, point3):
    hypotenuse1 = findDistance4326geodesic(convertPoint(point1), convertPoint(point2))
    hypotenuse2 = findDistance4326geodesic(convertPoint(point1), convertPoint(point3))
    hypotenuse3 = findDistance4326geodesic(convertPoint(point2), convertPoint(point3))
    p = (hypotenuse1 + hypotenuse2 + hypotenuse3) / 2
    try:
        return round(2 * math.sqrt(p * (p - hypotenuse1) * (p - hypotenuse2) * (p - hypotenuse3)) / hypotenuse3, 1)
    except:
        print(hypotenuse3)
        return 0


def getHeight4326_2(point1, point2, point3):
    leg5 = point2[0] - point3[0]
    leg6 = point2[1] - point3[1]
    hypotenuse1 = findDistance3857(point1, point2)
    hypotenuse2 = findDistance3857(point1, point3)
    hypotenuse3 = math.sqrt(pow(leg5, 2) + pow(leg6, 2))

    p = (hypotenuse1 + hypotenuse2 + hypotenuse3) / 2
    height = 2 * math.sqrt(p * (p - hypotenuse1) * (p - hypotenuse2) * (p - hypotenuse3)) / hypotenuse3

    if leg5 == 0:
        leg5 = 0.01
    side1 = point2[1] - leg6 / leg5 * point2[0]
    y4 = leg6 / leg5 * point1[0] + side1

    i = 0
    if point3[0] == point2[1]:
        if point1[0] > point3[0]:
            i -= 1
        else:
            i += 1
    elif (point3[0] > point2[0]) + (point1[1] > y4) == 1:
        i -= 1
    else:
        i += 1
    basePoint = [point1[0] - i * height * (point2[1] - point3[1]) / hypotenuse3,
                 point1[1] + i * height * (point2[0] - point3[0]) / hypotenuse3]

    return findDistance4326great_circle(convertPoint(point1), convertPoint(basePoint))


def getDirection(point1, point2):
    x_diff = point1[0] - point2[0]
    y_diff = point1[1] - point2[1]
    if x_diff == 0 or y_diff == 0:
        alpha = 0
    else:
        alpha = round(math.atan(y_diff / x_diff) * 180 / math.pi)
    if x_diff > 0:
        return alpha + 180
    else:
        if y_diff > 0:
            return alpha + 360
        else:
            return alpha


def cellBorders(coordinates):
    min_horizontal_point = 99999999
    min_vertical_point = 99999999
    max_horizontal_point = 0
    max_vertical_point = 0
    for _ in range(len(coordinates) - 1):
        if coordinates[_][0] < min_horizontal_point:
            min_horizontal_point = coordinates[_][0]
        if coordinates[_][0] > max_horizontal_point:
            max_horizontal_point = coordinates[_][0]
        if coordinates[_][1] < min_vertical_point:
            min_vertical_point = coordinates[_][1]
        if coordinates[_][1] > max_vertical_point:
            max_vertical_point = coordinates[_][1]

    return [min_horizontal_point, min_vertical_point, max_horizontal_point, max_vertical_point]


def getCell(point, min_point, cell_size):
    return [int((point[0] - min_point[0]) / cell_size) + 1,
            int((point[1] - min_point[1]) / cell_size) + 1]


def get4PolygonPoints(point1, point2, tractor_width):
    x_diff = point1[0] - point2[0]
    y_diff = point1[1] - point2[1]

    hypotenuse = math.sqrt(pow(x_diff, 2) + pow(y_diff, 2))
    length = tractor_width * y_diff / hypotenuse
    width = tractor_width * x_diff / hypotenuse
    return [(point1[0] - length, point1[1] + width), (point1[0] + length, point1[1] - width),
            (point2[0] + length, point2[1] - width), (point2[0] - length, point2[1] + width)]


def get2PolygonPoints(point1, point2, point3, tractor_width):
    x_diff = point1[0] - point3[0]
    y_diff = point1[1] - point3[1]

    hypotenuse = math.sqrt(pow(x_diff, 2) + pow(y_diff, 2))

    length = y_diff / hypotenuse * tractor_width
    width = x_diff / hypotenuse * tractor_width
    return [(point2[0] - length, point2[1] + width), (point2[0] + length, point2[1] - width)]


def calculate(point1, point2, point3):
    # Так же находим все расстояния от точек друг от друга
    leg1 = point1[0] - point2[0]
    leg2 = point1[1] - point2[1]
    leg5 = point2[0] - point3[0]
    leg6 = point2[1] - point3[1]
    hypotenuse1 = math.sqrt(pow(leg1, 2) + pow(leg2, 2))
    hypotenuse2 = findDistance3857(point1, point3)
    hypotenuse3 = math.sqrt(pow(leg5, 2) + pow(leg6, 2))

    # Отношения сторон в треуголнике построенным Point2 и Point3
    sinS = leg5 / hypotenuse3
    cosS = leg6 / hypotenuse3

    # Синус угла Point2-newMiddlePoint-Point3
    sinXY = math.acos(
        (pow(hypotenuse1, 2) + pow(hypotenuse2, 2) - pow(hypotenuse3, 2)) / (2 * hypotenuse1 * hypotenuse2))

    # Того же угла но в 2 раза меньше (угол биссектрисы)
    sinXY2 = math.sin(sinXY / 2)
    # Косинус угла sinXY2

    # Расстояние между Point2-newMiddlePoint либо Point3-newMiddlePoint
    hypotenuse4 = hypotenuse3 / (2 * math.sqrt(1 - pow(sinXY2, 2)))

    # Расстояние между newMiddlePoint и серединой Point2-Point3
    leg7 = sinXY2 * hypotenuse4

    # # для определения направления
    if leg1 == 0:
        leg1 = 0.01
    side1 = point2[1] - leg2 / leg1 * point2[0]
    y4 = leg2 / leg1 * point3[0] + side1

    i = 0
    if point1[0] == point2[1]:
        if point1[0] < point3[0]:
            i -= 1
        else:
            i += 1
    elif (point1[0] > point2[0]) + (point3[1] > y4) == 1:
        i -= 1
    else:
        i += 1

    return [leg5 / 2 + point3[0] + i * cosS * leg7, leg6 / 2 + point3[1] - i * sinS * leg7]


def addRoundedPoints(i, point1, point2, point3, coordinates):
    # Находим расстояния всех точек друг от друга
    x_diff = point1[0] - point2[0]
    y_diff = point1[1] - point2[1]
    # Не использована функция findDistance3857 так как x_diff и y_diff нужны в алгоритме
    hypotenuse1 = math.sqrt(pow(x_diff, 2) + pow(y_diff, 2))
    hypotenuse2 = findDistance3857(point1, point3)
    hypotenuse3 = findDistance3857(point2, point3)

    # Это на случай если все 3 точки на одной прямой
    if abs(hypotenuse1 + hypotenuse3 - hypotenuse2) < 0.1:
        return

    # Находим угол с вершиной на 2 точке
    sinXY = math.acos(
        (pow(hypotenuse1, 2) + pow(hypotenuse3, 2) - pow(hypotenuse2, 2)) / (2 * hypotenuse1 * hypotenuse3))

    # Удаляет точку при маленькой длине
    # В будущем надо доработать чтобы избавится от этой функций
    if hypotenuse3 < 6:
        del coordinates[i]

    # При маленьком угле точки (то есть не пряамая линия)
    if sinXY < math.pi / 1.7:

        # Точка которая на линий hypotenuse1 которая равноудалена от Point2 c Point3
        newMiddlePoint = [point2[0] + hypotenuse3 * x_diff / hypotenuse1,
                          point2[1] + hypotenuse3 * y_diff / hypotenuse1]
        # Оснавание биссектрисы на окруженность которая построена вокруг newMiddlePoint-Point2-Point3
        newRoundedPoint = calculate(newMiddlePoint, point2, point3)
        # Если newMiddlePoint не дальше от Point1 то добавляем точку
        if hypotenuse1 > hypotenuse3:
            coordinates.insert(i + 1, newMiddlePoint)
            coordinates.insert(i + 3, newRoundedPoint)
        # Если нет то она не нужна
        else:
            coordinates.insert(i + 2, newRoundedPoint)
        # Подробное описание в картинке номер 3
        return
