from shapely.geometry import Polygon

from tractor import *
from lattice import *
from bokeh.plotting import figure
from bokeh.io import show


def drawXY(coordinates, polygons, overlaps, plot_size):
    p = figure(plot_width=plot_size[0], plot_height=plot_size[1],
               title='Example Chart',
               x_axis_label='X', y_axis_label='Y')

    x_list = []
    y_list = []
    x_list2 = []
    y_list2 = []

    for i in polygons:
        try:
            coord = list(zip(*i.exterior.coords.xy))
            coord.append(coord[0])  # repeat the first point to create a 'closed loop'
            xs, ys = zip(*coord)  # create lists of x and y values
            x_list.append([[list(xs)]])
            y_list.append([[list(ys)]])
        except:
            pass

    xs, ys = zip(*coordinates)

    p.line(list(xs), list(ys), line_width=1)

    p.multi_polygons(x_list, y_list, color="red", fill_alpha=0.2)

    for i in overlaps:
        try:
            coord = list(zip(*i.exterior.coords.xy))
            coord.append(coord[0])  # repeat the first point to create a 'closed loop'
            xs, ys = zip(*coord)  # create lists of x and y values
            x_list2.append([[list(xs)]])
            y_list2.append([[list(ys)]])
        except:
            pass
    p.multi_polygons(x_list2, y_list2, color="green", fill_alpha=0.5)

    show(p)


class getOverlap(Tractor):
    def __init__(self, url):
        super().__init__(url)
        self.polygons = []
        self.overlaps = []
        self.tractor_width = 10
        self.lattice = lattice()
        self.addMiddlePoints()
        self.create_grid()
        self.createPolygons()

    # https://www.youtube.com/watch?v=Qgevy75co8c
    # num.py
    def create_grid(self):
        borders = cellBorders(self.coordinates)
        grid_size = math.sqrt(pow(self.line_limit, 2) + pow(self.tractor_width, 2))
        self.lattice.set_grid([borders[0], borders[1]], [borders[2], borders[3]],
                              grid_size)

    def createPolygons(self):

        previous_Points = 0
        i = 0
        while i < len(self.coordinates):

            if i < len(self.coordinates) - 2:
                addRoundedPoints(i, self.coordinates[i], self.coordinates[i + 1],
                                 self.coordinates[i + 2], self.coordinates)
            parsedGridPoint = getCell([(self.coordinates[i - 1][0] + self.coordinates[i][0]) / 2,
                                       (self.coordinates[i - 1][1] + self.coordinates[i][1]) / 2],
                                      self.lattice.get_min_point(), self.lattice.get_cell_size())
            if i == 0:
                previous_Points = get4PolygonPoints(self.coordinates[0], self.coordinates[1],
                                                    self.tractor_width)

            elif i == len(self.coordinates) - 1:
                current_Points = get4PolygonPoints(self.coordinates[i - 1], self.coordinates[i],
                                                   self.tractor_width)

                current_Polygon = Polygon([current_Points[0], current_Points[1],
                                           current_Points[2], current_Points[3]]).convex_hull
                self.polygons.append(current_Polygon)
                for y in range(3):
                    for z in range(3):
                        for l in range(
                                len(self.lattice.get_grid(
                                    [parsedGridPoint[0] - 1 + y, parsedGridPoint[1] - 1 + z]))):
                            comparative_Polygon = \
                                self.lattice.get_grid([parsedGridPoint[0] - 1 + y, parsedGridPoint[1] - 1 + z])[l]
                            if current_Polygon.intersects(comparative_Polygon):
                                try:
                                    self.overlaps.append(Polygon(current_Polygon.intersection(comparative_Polygon)))
                                except:
                                    print("Error")
                self.lattice.get_grid(parsedGridPoint).append(current_Polygon)
            else:

                current_Points = get2PolygonPoints(self.coordinates[i - 1], self.coordinates[i],
                                                   self.coordinates[i + 1], self.tractor_width)

                current_Polygon = Polygon(
                    [previous_Points[0], previous_Points[1], current_Points[0], current_Points[1]]).convex_hull
                self.polygons.append(current_Polygon)
                #  if type(current_Polygon) is Polygon else current_Polygon.buffer()
                previous_Points = [current_Points[1], current_Points[0]]

                for y in range(3):
                    for z in range(3):
                        for l in range(
                                len(self.lattice.get_grid(
                                    [parsedGridPoint[0] - 1 + y, parsedGridPoint[1] - 1 + z]))):
                            comparative_Polygon = \
                                self.lattice.get_grid([parsedGridPoint[0] - 1 + y, parsedGridPoint[1] - 1 + z])[l]
                            try:
                                if current_Polygon.intersects(comparative_Polygon):
                                    convexed_Polygon = current_Polygon.intersection(comparative_Polygon).convex_hull
                                    self.overlaps.append(convexed_Polygon if type(
                                        convexed_Polygon) is Polygon else convexed_Polygon.buffer())
                            except:
                                pass
                self.lattice.get_grid([parsedGridPoint[0], parsedGridPoint[1]]).append(current_Polygon)
            i += 1

        print("Only draw left")
        plot_size = [1000, int(1000 * self.lattice.grid_vertical_size / self.lattice.grid_horizontal_size)]
        drawXY(self.coordinates, self.polygons, self.overlaps, plot_size)

