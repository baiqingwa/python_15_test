# -*- coding: utf-8 -*-#
# Name:         recharge
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/16 0016

import unittest
from ddt import ddt, data  # 装饰器
from week_10_API_learn.common import study_session_requests
from week_10_API_learn.common.Do_excel import DoExcel
from week_10_API_learn.common.contents_ml import case_file
from week_10_API_learn.common.Mysql_data import Mysql
from week_10_API_learn.common import re_data


@ddt  # @ddt装饰测试类 unittest.TestCase的子类
class TestAdd(unittest.TestCase):
    '''自动化测试框架，完成接口自动化'''
    # 1.创建操作excel的实例化对象,拿到测试数据
    do_excel = DoExcel(case_file, 'recharge')
    cases = do_excel.get_cases()

    @classmethod
    #执行一次
    def setUpClass(cls):
        # 1.创建所需对象，方便调用方法（请求、数据库）
        cls.http_request = study_session_requests.HttpRequest_session()
        cls.mysql=Mysql()

    @data(*cases)
    def test_recharge(self, case):
        # 1.判断是否需要数据校验（充值前的余额）
        if case.sql is not None:
            before_amount = self.mysql.get_fetch_one(eval(case.sql)['sql1'])['leaveamount']
            print('充值前的余额:',before_amount)
        # 2.在请求之前替换参数化的值
        case.data = re_data.replace(case.data)
        # 3.接口请求,获取响应状态码
        resp = self.http_request.request(case.method, case.url, case.data)
        actual_code = resp.json()['code']
        print('''执行第{}条用例：
                                 title:{}
                                 请求参数：{}
                                 请求方法：{}
                                 请求地址：{}\n
                                 expected:{}
                                 actual:{}
                                 '''.format(case.case_id, case.title, case.data, case.method, case.url, case.expected,resp.text))
        #4.判断是否需要数据校验（充值之后的余额）
        if case.sql is not None:
            after_amount=self.mysql.get_fetch_one(eval(case.sql)['sql1'])['leaveamount']
            print('充值之后的余额:',after_amount)
        #5.获取充值的金额
            recharge_amout=int(eval(case.data)['amount'])
            print(recharge_amout)
        #6.进行断言(响应结果、充值金额是否匹配)
            self.assertEqual(before_amount + recharge_amout, after_amount)
        try:
            self.assertEqual(str(case.expected), actual_code)
            self.do_excel.write_result(case.case_id + 1, resp.text, 'PASS')
        except AssertionError as e:
            self.do_excel.write_result(case.case_id + 1, resp.text, 'FAIL')
            raise e

    @classmethod
    #执行一次
    def tearDownClass(cls):
        # 1.关闭需要关闭的内容
        cls.http_request.close()  # 关闭session对象，清除cookies
        cls.mysql.close()         # 关闭数据库连接