import urllib
from pyheatmap.heatmap import HeatMap


def main():

    url = "https://raw.github.com/oldj/pyheatmap/master/examples/test_data.txt"
    print "begin"
    sdata = urllib.urlopen(url).read().split("\n")
    data = []
    for ln in sdata:
        a = ln.split(",")
        if len(a) != 2:
            continue
        a = [int(i) for i in a]
        data.append(a)

    hm = HeatMap(data)
    hm.heatmap(save_as="heat.png")


if __name__ == "__main__":
    main()