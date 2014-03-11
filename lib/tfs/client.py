#
# Python TFS WebService Client
#
__all__ = ["TFSClient"]

import logging
import httplib2
import random
import simplejson as json


class TFSClient:
    """TFS Webservice Client Operator class."""
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', logging.getLogger())
        self.app_key = kwargs.get('app_key', None)
        self.host = kwargs.get('root_server', None)
        self.rest = RestHelper(logger=self.logger)
        if not self._initNgxServerList():
            raise Exception, 'init ngx server list failed.'

    def _initNgxServerList(self):
        """init ngx server list from root_server"""
        self.ngx_server_list = []
        self.ngx_req_limit = 0
        ret = self.rest.get(self.host, '/url.list', {})
        if ret == False:
            return False
        _flist = ret.strip().split("\n")

        self.ngx_req_limit = _flist.pop(0)

        for l in _flist:
            if l.find(':') < 0:
                continue
            self.ngx_server_list.append(l)
        self._setNgxServer()
        return True

    def _setNgxServer(self):
        self.ngx_server = self.ngx_server_list[random.randint(0, len(self.ngx_server_list) - 1)]

    def writeFile(self, content):
        """write content to tfs, return is file name"""
        size = len(content)
        ret = self.rest.post(self.ngx_server, self.getUrl() + '?suffix=.jpg', content, {'Content-Length': str(size)})
        if ret == False:
            self.logger.error('write file to tfs failed.')
            raise Exception, 'write file to tfs failed.'
        try:
            json_obj = json.loads(ret)
        except Exception, e:
            self.logger.error('decode tfs return failed: %s' % e)
            raise Exception, 'decode tfs return failed: %s' % e
        if not json_obj:
            self.logger.error('tfs return is empty')
            raise Exception, 'tfs return is empty'
        file_name = json_obj['TFS_FILE_NAME']
        self.logger.info('Upload Tfs file:%s size:%s' % (file_name, size))
        return file_name

    def delFile(self, file_name):
        """delete file from tfs"""
        ret = self.rest.delete(self.ngx_server, self.getUrl() + '/' + file_name, {}, [200, 404])
        if ret == False:
            self.logger.error('delete file:%s from tfs failed.' % file_name)
            raise Exception, 'delete file:%s from tfs failed.' % file_name
        self.logger.info('Delete Tfs file: %s' % file_name)
        return True

    def getUrl(self):
        return '/v1/' + str(self.app_key)

    def __del__(self):
        del self.logger
        del self.rest


class RestHelper:
    """http rest web service helper"""
    def __init__(self, **kwargs):
        """Restful webservice helper class."""
        self.logger = kwargs.get('logger', logging.getLogger())
        self.http = httplib2.Http(timeout=2)

    def get(self, host, url, headers, allow_code=[200]):
        return self._connect(host, url, '', 'GET', headers, allow_code)

    def post(self, host, url, body, headers, allow_code=[200]):
        return self._connect(host, url, body, 'POST', headers, allow_code)

    def delete(self, host, url, headers, allow_code=[200]):
        return self._connect(host, url, '', 'DELETE', headers, allow_code)

    def _connect(self, host, url, body, method, headers, allow_code):
        """send http request to host"""
        _compact_url = 'http://' + host + '' + url
        try:
            (response, content) = self.http.request(_compact_url, method=method, body=body, headers=headers)
        except Exception, e:
            self.logger.error("rest failed:: host: %s;; url: %s;; body: -;; method: %s;; headers: %s;;error: %s"
                              % (host, url, method, headers, e))
            return False

        if not (response.status in allow_code):
            self.logger.error("rest reponse error:: host: %s;; url: %s;; body: -;; method: %s;; headers: %s;; reponse header: %s;; reason: %s;;allow: %s"
                              % (host, url, method, headers, response.status, response.reason, allow_code))
            return False

        self.logger.debug("rest request host: %s;; url: %s;; body: -;; method: %s;; headers: %s;; reponse header: %s;; reason: %s;;"
                          % (host, url, method, headers, response.status, response.reason))
        return content

    def __del__(self):
        del self.logger
        del self.http


