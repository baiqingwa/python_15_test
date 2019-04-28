# -*- coding: utf-8 -*-#
# Name:         contents_获取目录
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/13 0013

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

case_file = os.path.join(base_dir, 'data', 'cases.xlsx') #层层定位

open_file = os.path.join(base_dir, 'config', 'open.conf') #层层定位

Online_file = os.path.join(base_dir, 'config', 'Online.conf') #层层定位

test_file = os.path.join(base_dir, 'config', 'test.properties') #层层定位

db_file = os.path.join(base_dir, 'config', 'db_data.conf') #层层定位

log_file = os.path.join(base_dir, 'log')

reports_file = os.path.join(base_dir, 'reports')

case_dir = os.path.join(base_dir,'testcases')
