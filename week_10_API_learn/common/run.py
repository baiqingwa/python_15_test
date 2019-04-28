# -*- coding: utf-8 -*-#
# Name:         run
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/26 0026

import unittest
from week_10_API_learn.common.contents_ml import reports_file,case_dir
import HTMLTestRunnerNew
#hello
discover=unittest.defaultTestLoader.discover(case_dir,"test_*.py")

with open(reports_file+'/report.html','wb+') as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                     title='py_15测试报告',
                                     verbosity=2,
                                     description='关于全程贷的测试报告',
                                     tester='baiqing')
    runner.run(discover)