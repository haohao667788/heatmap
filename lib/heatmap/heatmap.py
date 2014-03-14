import os
import Image
import ImageDraw2

from inc import cf

class HeatMap(object):

    def __init__(self, data, base=None, width=0, height=0):

        assert type(data) in (list, tuple)
        assert base is None or os.path.isfile(base)
        assert type(width) in (int, long, float)
        assert type(height) in (int, long, float)
        assert width >= 0 and height >= 0

        self.data = data
        self.base = base
        self.width = width
        self.height = height
        self.max_data = []

        if not self.base and (self.width == 0 or self.height == 0):
            w, h = cf.getMaxSize(data)
            self.width = self.width or w
            self.height = self.height or h


    def __mkImg(self, base=None):

        base = base or self.base

        if base:
            self.__im = Image.open(base) if type(base) in (str, unicode) else base
            self.width, self.height = self.__im.size
        else:
            self.__im = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))


    def __heat(self, heat_data, x, y, n, t, template):

        l = len(heat_data)
        width = self.width
        p = width * y + x

        for ip, iv in template:
            p2 = p + ip
            if 0 <= p2 < l:
                if t == 0:
                    heat_data[p2] += iv * (0.8 * n)
                elif t == 1:
                    heat_data[p2] += iv * (2 + n)#(iv * n) * 12
                else:
                    heat_data[p2] += iv * (5 + n)#n * 30



    def __paintHeat(self, heat_data, colors):

        import re

        im = self.__im
        rr = re.compile(", (\d+)%\)")
        dr = ImageDraw2.ImageDraw.Draw(im)
        width = self.width
        height = self.height

        max_v = max(heat_data)
        if max_v <= 0:
            return

        print("max: %d" % max_v)

        r = 240.0 / max_v

        heat_data2 = []
        for i in heat_data:
            if i > 0:
                heat_data2.append(int(i * r) - 1)
            else:
                heat_data2.append(0)
        # heat_data2 = [int(i * r) - 1 for i in heat_data]

        size = width * height
        for p in xrange(size):
            v = heat_data2[p]
            if v > 0:
                x, y = p % width, p // width
                color = colors[v]
                alpha = int(rr.findall(color)[0])
                if alpha > 50:
                    al = 255 - 255 * (alpha - 50) / 50
                    im.putpixel((x, y), (0, 0, 255, al))
                else:
                    dr.point((x, y), fill=color)


    def heatmap(self, save_as=None, base=None, data=None):

        self.__mkImg()

        circle = cf.mkCircle(8, self.width)
        heat_data = [0] * self.width * self.height

        data = data or self.data

        for hit in data:
            x, y, n, t = hit
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                continue
            self.__heat(heat_data, x, y, n, t, circle)

        self.__paintHeat(heat_data, cf.mkColors())

        if save_as:
            self.save_as = save_as
            self.__save()

        return self.__im

    def __save(self):

        save_as = os.path.join(os.getcwd(), self.save_as)
        folder, fn = os.path.split(save_as)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        self.__im.save(save_as)
        self.__im = None


def test():

    print("load data...")
    mins = []
    data = []

    url = 'http://apluspre.taobao.ali.com/aplus/pub/udataResult.htm?spmId=a3109.6190702&action=udataAction&event_submit_do_getHotData=y'
    sdata = urllib.urlopen(url).read().split("\n")
    # f = open('ran_data.txt')
    for ln in sdata:
        a = ln.split(",")
        if len(a) != 4 or abs(int(a[0])) > 700 or int(a[1]) > 8500:
            continue
        mins.append(int(a[0]))

    imin = min(mins)
    if imin >= 0:
        imin = 0

    # f.seek(0)
    count = 0
    for ln in sdata:
        a = ln.split(",")
        if len(a) != 4:
            continue
        a = [int(a[0])-imin, int(a[1]), int(a[2]), int(a[3])]
        data.append(a)
        count += 1
    # f.close()

    starttime = time.clock()
    print("total lines: %d" % count)
    print("painting..")
    hm = HeatMap(data, None, 1400, 8500)
    hm.heatmap(save_as="heat.png")
    endtime = time.clock()
    print (endtime-starttime)
    print("done.")


if __name__ == "__main__":
    test()