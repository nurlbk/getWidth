import time

from getOverlap import *
from getWidth import *


def main():
    start_time = time.time()

    url = "routes/tractor 2.2.geojson"

    tractorA = getWidth(url, 3)
    print("Probably Widths =", tractorA.getProbablyWidth())
    print("--- getWidth %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
