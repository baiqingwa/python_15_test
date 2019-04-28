# -*- coding: utf-8 -*-#
# Name:         test_add_loan
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/20 0020
import unittest
from ddt import ddt,data
from week_10_API_learn.common.Do_excel import DoExcel
from week_10_API_learn.common.contents_ml import case_file
from week_10_API_learn.common.study_session_requests import HttpRequest_session
from week_10_API_learn.common import re_data
from week_10_API_learn.common.log import r_log

@ddt
class AddTest(unittest.TestCase):
    # 1.创建操作excel的实例化对象,拿到测试数据
    excel = DoExcel(case_file, 'add_loan')
    cases = excel.get_cases()
    log=r_log(__name__)

    @classmethod
    def setUpClass(cls):
        # 1.创建所需对象，方便调用方法（request请求）
        cls.http_request = HttpRequest_session()

    @data(*cases)
    def test_add(self, case):
        # case.data = eval(case.data)  # 变成字典
        # print(type(case.data))
        # if case.data.__contains__('mobilephone') and case.data['mobilephone'] == 'normal_user':
        #     case.data['mobilephone'] = config.get('data', 'normal_user')  # 拿到配置文件里面的值赋值给mobilephone
        #
        # if case.data.__contains__('pwd') and case.data['pwd'] == 'normal_pwd':
        #     case.data['pwd'] = config.get('data', 'normal_pwd')  # 拿到配置文件里面的值赋值给mobilephone
        #
        # if case.data.__contains__('memberId') and case.data['memberId'] == 'loan_member_id':
        #     case.data['memberId'] = config.get('data', 'loan_member_id')  # 拿到配置文件里面的值赋值给mobilephone
        #1.在请求之前替换参数化的值
        case.data = re_data.replace(case.data)
        resp = self.http_request.request(case.method, case.url, case.data)
        #收集日志
        self.log.critical('''执行第{}条用例：
                         title:{}
                         请求参数：{}
                         请求方法：{}
                         请求地址：{}\n
                         expected:{}
                         actual:{}
                         '''.format(case.case_id, case.title, case.data, case.method, case.url, case.expected,resp.text))
        #2.断言结果
        try:
            self.assertEqual(case.expected, resp.text)
            self.excel.write_result(case.case_id + 1, resp.text, 'PASS')
            print(resp.json())

        except AssertionError as e:
            self.excel.write_result(case.case_id + 1, resp.text, 'FAIL')
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()
