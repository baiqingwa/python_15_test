# -*- coding: utf-8 -*-#
# Name:         log
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/25 0025

#写一个日志类
#结合配置文件 完成 输出的格式 输出的级别的配置
import logging
from week_10_API_learn.common.config import cf
from week_10_API_learn.common.contents_ml import log_file
class r_log:
    '''读取日志信息'''
    def __init__(self,name):
        self.Level_1 = cf.get_values('LOG', 'level_1')
        self.Level_2 = cf.get_values('LOG', 'level_2')
        self.formatter = cf.get_values('LOG', 'formatter')

        self.fmt = logging.Formatter(self.formatter)  # 指定格式

        self.My_logger = logging.getLogger(name)  # 创建的收集器
        self.My_logger.setLevel(self.Level_1)  # 设定收集信息的级别

        self.My_FileHandler = logging.FileHandler(log_file+'/log.txt',encoding='utf-8')  # 创建的输出器
        self.My_FileHandler.setLevel(self.Level_2)  # 设定输出信息的级别
        self.My_FileHandler.setFormatter(self.fmt)  # 指定格式

        self.MY_StreamHandler = logging.StreamHandler()
        self.MY_StreamHandler.setLevel(self.Level_2)
        self.MY_StreamHandler.setFormatter(self.fmt)

        self.My_logger.addHandler(self.My_FileHandler) # 配合收集器和输出器
        self.My_logger.addHandler(self.MY_StreamHandler)
    def debug(self,q):
        self.My_logger.debug(q)
    def info(self,q):
        self.My_logger.info(q)
    def warning(self,q):
        self.My_logger.warning(q)
    def error(self,q):
        self.My_logger.error(q)
    def critical(self,q):
        self.My_logger.critical(q)
