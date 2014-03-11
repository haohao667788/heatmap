import urllib
import math

from django.http import HttpResponse

from pyheatmap.heatmap import HeatMap

def getHeatMap(request):


    url = "https://raw.github.com/oldj/pyheatmap/master/examples/test_data.txt"
    sdata = urllib.urlopen(url).read().split("\n")
    mins = []
    data = []
    for ln in sdata:
        a = ln.split(",")
        if len(a) != 3:
            continue
        mins.append(int(a[0]))

    imin = min(mins)

    for ln in sdata:
        a = ln.split(",")
        if len(a) != 3:
            continue
        a = [int(a[0])+imin, int(a[1]), int(a[2])]
        data.append(a)

    hm = HeatMap(data, None, 1400, 10000)
    hm.heatmap(save_as="heat.png")

    return HttpResponse("complete")