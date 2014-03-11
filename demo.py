#!/usr/bin/env python

import logging
import sys

from client import TFSClient
logging.basicConfig(filename='./a.log')
tfs = TFSClient(app_key='4f0fc2de88dec',
                root_server='restful-store.daily.tbsite.net:3800',
                logger=logging.getLogger())

f = './demo/t5.jpg'
img_file = open(f, 'r')
img_content = img_file.read()
img_file.close()

# upload file to tfs
tfs_img_file = tfs.writeFile(img_content)
print 'upload local image:%s to tfs:%s' % (f, tfs_img_file)

# delete file from tfs
ret = tfs.delFile(tfs_img_file)
if ret == True:
    print 'delete tfs file:%s succ.' % tfs_img_file
else:
    print 'delete tfs file:%s failed.' % tfs_img_file


print 'Done.'
sys.exit(0)


