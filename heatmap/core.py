import urllib
import random
import time

from pyheatmap.heatmap import HeatMap

def ran_data():

    f = open('../example/test1.txt', 'w')
    for i in range(10):
        x = random.randint(-1400, 1400)
        y = random.randint(0, 15000)
        cnt = random.randint(1, 100)
        f.write('%i, %i, %i\n' % (x, y, cnt))

    f.close()
    print("finish")


def test():

    print("load data..")
    mins = []
    data = []

    url = 'http://apluspre.taobao.ali.com/aplus/pub/udataResult.htm?spmId=1.6659421&action=udataAction&event_submit_do_getHotData=y'
    sdata = urllib.urlopen(url).read().split("\n")
    for ln in sdata:
        a = ln.split(",")
        if len(a) != 3 or abs(int(a[0])) > 700 or int(a[1]) > 10000:
            continue
        mins.append(int(a[0]))

    imin = min(mins)
    if imin >= 0:
        imin = 0

    for ln in sdata:
        a = ln.split(",")
        if len(a) != 3:
            continue
        a = [int(a[0])-imin, int(a[1]), int(a[2])]
        data.append(a)

    starttime = time.clock()
    print("painting..")
    hm = HeatMap(data, None, 1400, 10000)
    hm.heatmap(save_as="heat.png")
    endtime = time.clock()
    print (endtime-starttime)
    print("done.")


if __name__ == "__main__":
    test()