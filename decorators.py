#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import threading
import time
import os
import sys
import platform


def chdir(adir=''):
    """自动调用os.chdir

    :param adir:
    :return:
    """
    def _chdir(func):
        def __chdir(*args, **kwargs):
            # print adir
            os.chdir(adir)
            return func(*args, **kwargs)
        return __chdir
    return _chdir


def retry(times=5):
    """一个装饰器，可以设置报错重试次数

    :param times: 最多重试次数
    :return:
    """
    def _retry(func):
        def __retry(*args, **kwargs):
            temp_count = 0
            while temp_count <= times:
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception:
                    print sys.exc_value
                    temp_count += 1
                    if temp_count <= times:
                        print '1秒后重试第{0}次'.format(temp_count)
                        time.sleep(1)
            else:
                print 'max try,can not fix'
                import traceback
                traceback.print_exc()
                return None
        return __retry
    return _retry


def count_running_time(func):
    """装饰器函数，统计函数的运行耗时

    :param func:
    :return:
    """
    def _count_running_time(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('cost time :{0}'.format(time.time() - start))
        return res
    return _count_running_time


def auto_next(func):
    """可以给协程用，自动next一次

    :param func:
    :return:
    """
    def _auto_next(*args, **kwargs):
        g = func(*args, **kwargs)
        g.next()
        return g
    return _auto_next


def check_adb(func):
    def _check_adb(*args, **kwargs):
        from utils import android
        result = android.get_adb_devices()
        if(len(result)) < 2:
            print '当前没有连接上手机'
            return None
        return func(*args, **kwargs)
    return _check_adb


def run_once(func):
    """60秒内，直接返回结果，不再重复运行

    :param func:
    :return:
    """
    def _run_once(*args, **kwargs):
        if (not _run_once.result) or (time.time()-_run_once.last_update_time > 60):
            # print 'no result or >60'
            _run_once.result = func(*args, **kwargs)
            _run_once.last_update_time = time.time()
        # else:
        #     print 'has result {}'.format(_run_once.result)
        return _run_once.result
    _run_once.result = None
    _run_once.last_update_time = 0
    return _run_once


def windows(func):
    """如果非windows系统，抛出异常

    :param func:
    :return:
    """

    if not platform.platform().startswith('Windows'):
        raise Exception("This function just can be used in windows.")
    return func


class Singleton(object):
    """单例模式，python最佳的单例方式还是通过模块来实现

    用法如下:
        @Singleton
        class YourClass(object):
    """
    def __init__(self, cls):
        self.__instance = None
        self.__cls = cls
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        self._lock.acquire()
        if self.__instance is None:
            self.__instance = self.__cls(*args, **kwargs)
        self._lock.release()
        return self.__instance


if __name__ == '__main__':

    import datetime
    print datetime.datetime(2011,4,2,13,15,16)
    print time.time()