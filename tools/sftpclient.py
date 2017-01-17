#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import paramiko
import time
import os
# import progressbar

from utils.tools.minipb import MiniProgressBar

"""
SFTP到内网，可以下载服务器端配置
更新日期：2016-1-9
"""


class SFTPClient(object):

    def __init__(self, host, port, user, pwd):
        self.t = paramiko.Transport((host, port))
        self.t.connect(username=user, password=pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

    def _get_files_recursion(self, path, result=[]):
        """递归方式获取指定目录下的全部文件

        :param path:
        :param result:
        :return:
        """
        if not path.endswith('/'):
            path = '{0}/'.format(path)
        for i in self.sftp.listdir(path):
            if i.find('.') != -1:
                result.append("{0}{1}".format(path,i))
            else:
                self._get_files_recursion("{0}{1}/".format(path, i))
        return result

    def _get_files_yield(self, path):
        """遍历指定目录下的文件，返回文件地址的列表，生成器方式

        :param path:
        :return:
        """
        if not path.endswith('/'):
            path = '{0}/'.format(path)
        for i in self.sftp.listdir(path):
            if i.find('.') != -1:
                yield ("{0}{1}".format(path, i))
            else:
                for i in self._get_files_yield("{0}{1}/".format(path, i)):
                    yield i

    def _download(self, remote_path, download_dir):

        local_path = os.path.abspath(remote_path.replace('/data/www/sg/sg_dev/socket/conf/config', download_dir))
        dirname = os.path.dirname(local_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.sftp.get(remote_path, local_path)

    def pro_download(self, path, download_dir):

        # pro = progressbar.ProgressBar()
        for remote_path in MiniProgressBar(self._get_files_recursion(path)):
            self._download(remote_path, download_dir)

    def debug_download(self, path, download_dir):
        for remote_path in self._get_files_yield(path):
            print('start to download {0}'.format(remote_path))
            self._download(remote_path, download_dir)
            print('finish')

    def get_file_update_time(self, path):
        result = self.sftp.listdir_attr(path)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[0].st_mtime))

    def close(self):
        self.sftp.close()
        self.t.close()
