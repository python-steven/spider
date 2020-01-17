import os
import sys
import time
import logging
file_name = os.path.split(os.path.splitext(sys.argv[0])[0])[-1]
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')  #创建文件夹，
log_time = time.strftime("%Y-%m-%d.log", time.localtime())
class Rookie:
    def __getattr__(self, items):
        return getattr(self.logger, items)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func

    def __init__(self, set_level="INFO", name=file_name, log_name=log_time, log_path=file_path, role=True):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(filename)s -%(funcName)s-%(levelname)s-%(levelno)s -%(lineno)d-%(module)s-%(name)s: \n  %(message)s",
            datefmt="%Y-%m-%d  %H:%M:%S %p %a", )
        create_list = []
        create_list.append(logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8"))
        if role:
            create_list.append(logging.StreamHandler())
        for i in create_list:
            i.setFormatter(formatter)
            self.addHandler(i)
#a = Rookie("debug","200","steven.log",r"C:\Users\Z15123001\Desktop\log")
'''
%(asctime)s     :             '2003-07-08 16：49：45,896'的形式（逗号之后的数字是毫秒部分的时间）
%(filename)s   :  	路径名的文件名部分
%(funcName)s:             日志调用所在的函数名
%(levelname)s:              消息的级别名称('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
%(levelno)s    :                对应数字格式的日志级别 (DEBUG, INFO, WARNING, ERROR,CRITICAL)
%(lineno)d      :               发出日志记录调用的源码行号 (如果可用)。
%(module)s   :               所在的模块名(如test6.py模块则记录test6)
%(message)s :               记录的信息
%(name)s       :                调用的logger记录器的名称
%(process)d :                 进程ID
%(processName)s:       进程名
%(thread)d  :                  线程ID
%(threadName)s  :       线程名
'''
'''
实例化需要传入的信息依次为
信息等级 : ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')            可以不填("")，以最低的INFO为基准线
信息内容归类哪类：500,200,404,403......                                   可以不填("")，以调用的logger记录器的名字
产生的信息写入的文件名字：“steven.log”                                     可以不填("")，默认是创建log.log文件
#文件存放的路径：                                                         可以不填("")，默认是文件当前目录的路径

使用方法是
from rizhi import Rookie
logerbody=Rookie()

hoemin=os.environ.get("Path")# 这里是获取当前的环境变量是不是存在Path根据需求来加。。。。
def xuxuwen():
     b= Rookie()
     shang="xuxuwen"
     b.critical(shang+"\n critical"+str(hoemin))
xuxuwen()
'''
