# coding: utf-8
#
# author: gonghao.gh
# date: 2014-03-13
#

import urllib
import time
import random
import logging
import json
import os

from lib.heatmap.heatmap import HeatMap
from lib.tfs.client import TFSClient


# 设置 logging
logging.basicConfig(filename='./a.log')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 配置 tfs
tfs = TFSClient(app_key='4f0fc2de88dec',
                root_server='restful-store.daily.tbsite.net:3800',
                logger=logging.getLogger())

# 白名单
white_lists = [
    #'1.6659421'
    # ,
    # 'a1z09.1',
    # 'a1z0d.6639537',
    'a210c.1',
    # 'a1z0k.6846093',
    # 'a2107.1'
]


def ran_data():
    u""" 生成随机数据(测试用) """

    f = open('ran_data.txt', 'w')
    for i in range(2000):
        x = random.randint(1, 500)
        y = random.randint(1, 500)

        rand = random.randint(1, 100)
        if rand < 5:
            t = 0
            n = 500
        elif 5 <= rand < 35:
            t = 1
            n = random.randint(1, 20)
        else:
            t = 2
            n = 1

        f.write('%d,%d,%d,%d\n' % (x, y, n, t))

    f.close()


def run():
    u""" 执行定时热图生成任务 """

    for spm in white_lists:

        logger.info("#####loading data from %s#####" % spm)
        print("loading data from %s" % spm)

        url = 'http://apluspre.taobao.ali.com/aplus/pub/udataResult.htm?spmId=%s&action=udataAction&event_submit_do_getHotData=y' % spm
        sdata = urllib.urlopen(url).read().split("\n")

        # f = open('ran_data.txt')
        mins = []
        data = []
        for ln in sdata:
            a = ln.split(",")
            if len(a) != 4 or abs(int(a[0])) > 700 or int(a[1]) > 8500:
                continue
            mins.append(int(a[0]))

        imin = min(mins)
        if imin >= 0:
            imin = 0

        count = 0
        for ln in sdata:
            a = ln.split(",")
            if len(a) != 4:
                continue
            a = [int(a[0])-imin, int(a[1]), int(a[2]), int(a[3])]
            data.append(a)
            count += 1

        start_time = time.clock()
        logger.info("total lines: %d" % count)
        print("total lines: %d" % count)
        logger.info("painting..")
        print("painting..")
        hm = HeatMap(data, None, 1400, 8500)
        save_as = "heat_%s.png" % spm
        hm.heatmap(save_as=save_as)
        end_time = time.clock()
        logger.info(end_time - start_time)
        print(end_time - start_time)
        logger.info("%s done." % spm)
        print("%s done." % spm)

        logger.info("#"*20)
        print("#"*20)
        logger.info("start transform heat_%s" % spm)
        print("start transform heat_%s" % spm)

        f = './%s' % save_as
        img_file = open(f, 'r')
        img_content = img_file.read()
        img_file.close()

        tfs_img_file = tfs.writeFile(img_content)
        print 'upload local image:%s to tfs:%s' % (f, tfs_img_file)
        if tfs_img_file:
            url = 'http://apluspre.taobao.ali.com/aplus/pub/udataResult.htm?spmId=%s&action=udataAction&event_submit_doAddHotImage=y&image=%s' % (spm, tfs_img_file)

            n = 1
            while not n == 3:
                res = json.loads(urllib.urlopen(url).read())
                if not res["code"] == 200:
                    n += 1
                else:
                    break
        print 'upload success'
        os.remove(f)


if __name__ == "__main__":
    run()