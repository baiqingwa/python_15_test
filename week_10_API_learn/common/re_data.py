# -*- coding: utf-8 -*-#
# Name:         replace_参数化
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/20 0020

import re
from week_10_API_learn.common.config import cf
from configparser import ConfigParser

class Interface:
    loanID=None

def replace(data):
    '''进行参数化替换'''
    r="%(.*?)%"#正则表达式：获取需要替换的数据  #入坑$元字符$，纠结1个小时 百度发现$也是一个元字符 匹配输出行尾 555
    while re.search(r,data): #findall  字符串 任意位置 返回列表
        g=re.search(r,data)
        a=g.group(1)
        # print(a)
        #1.从配置文件中获取替换的值
        try:
            v=cf.get_values('data',a) #优化
        #2.配置文件里面没有的话，在interface这个类里面获取值
        except Exception as e:
            if hasattr(Interface,a):
                v=getattr(Interface,a)

        # print(v)
        #3.完成参数的替换
        data=re.sub(r,v,data,count=1)

    return data
if __name__ == '__main__':
    replace('{"mobilephone": "%user_mobilephone%", "pwd": "$user_pwd$"}')