# -*- coding: utf-8 -*-#
# Name:         login
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/16 0016
import unittest
from ddt import ddt, data  # 装饰器
from week_10_API_learn.common import study_session_requests
from week_10_API_learn.common.Do_excel import DoExcel
from week_10_API_learn.common.contents_ml import case_file




@ddt  # @ddt装饰测试类 unittest.TestCase的子类
class TestAdd(unittest.TestCase):
    '''自动化测试框架，完成接口自动化'''
    do_excel = DoExcel(case_file,'login')  # 创建操作excel的实例化对象
    cases = do_excel.get_cases()
    @classmethod
    def setUpClass(cls):
        cls.http_request = study_session_requests.HttpRequest_session() #创建请求实例化对象，方便调用方法

    @data(*cases)
    def test_Login(self,case):

        resp = self.http_request.request(case.method, case.url, case.data)
        actual=resp.text

        try:
            self.assertEqual(case.expected, actual)
            self.do_excel.write_result(case.case_id + 1, actual, 'PASS')
        except AssertionError as e:
            self.do_excel.write_result(case.case_id + 1, actual, 'FAIL')
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()  # 关闭session对象，清除cookies
