# -*- coding: utf-8 -*-#
# Name:         run_case
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/15 0015


from configparser import ConfigParser
from  week_10_API_learn.common.contents_ml import *

class r_configparser:
    '''打开配置文件，读取各种数据类型的数据'''

    def __init__(self):   #配置文件，编码格式
        self.cf=ConfigParser()
        self.cf.read(open_file,encoding='utf-8')
        #判断开关——进入哪个服务器
        if self.cf.getboolean('switch','open'):
            self.cf.read(Online_file,encoding='utf-8')
        else:
            self.cf.read(test_file,encoding='utf-8')

    def get_section(self):
        return self.cf.sections()

    def get_option(self,section):
        return self.cf.options(section)

    def get_values(self,section,option):
        return self.cf.get(section,option)

    def get_getint(self,section,option):
        return self.cf.getint(section,option)

    def get_getboolean(self,section,option):
        return self.cf.getboolean(section,option)

    def get_getfloat(self,section,option):
        return self.cf.getfloat(section,option)

cf=r_configparser()




