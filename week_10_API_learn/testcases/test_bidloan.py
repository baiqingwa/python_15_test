# -*- coding: utf-8 -*-#
# Name:         test_bidloan
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/24 0024

import unittest
from ddt import ddt,data
from week_10_API_learn.common.Do_excel import DoExcel
from week_10_API_learn.common.contents_ml import case_file
from week_10_API_learn.common.study_session_requests import HttpRequest_session
from week_10_API_learn.common import re_data
from week_10_API_learn.common import Mysql_data

@ddt
class AddTest(unittest.TestCase):
    # 1.创建操作excel的实例化对象,拿到测试数据
    excel = DoExcel(case_file, 'bidLoan')
    cases = excel.get_cases()

    @classmethod
    def setUpClass(cls):
        # 1.创建所需对象，方便调用方法（请求、数据库）
        cls.http_request = HttpRequest_session()
        cls.mysql=Mysql_data.Mysql()

    @data(*cases)
    def test_bidloan(self, case):

        #1.在请求之前替换参数化的值
        case.data = re_data.replace(case.data)
        #2.发送requests请求 响应结果
        resp = self.http_request.request(case.method, case.url, case.data)
        print('''执行第{}条用例：
                 title:{}
                 请求参数：{}
                 请求方法：{}
                 请求地址：{}\n
                 expected:{}
                 actual:{}
                 '''.format(case.case_id,case.title,case.data,case.method,case.url,case.expected,resp.text))
        print('json:',resp.json())
        #3.断言结果
        try:
            self.assertEqual(case.expected, resp.text)
            self.excel.write_result(case.case_id + 1, resp.text, 'PASS')
            #4.数据库校验
            if resp.json()['msg'] == '加标成功':
                #判断加标成功member_id=标的表的memberid
                try:
                    sql = 'select memberid from future.loan where memberid=1006 order by id desc limit 1'
                    self.assertEqual(eval(case.data)['memberId'],self.mysql.get_fetch_one(sql)['memberid'])
                except Exception as e:
                    print('验证失败，错误：{}，数据库没有对应的数据'.format(e))
                #将加标接口的标的id存储便于修改标的状态
                sql="select id from future.loan where memberid=1006 order by id desc limit 1"
                a=self.mysql.get_fetch_one(sql)['id']
                setattr(re_data.Interface,'loanID',str(a))

        except AssertionError as e:
            self.excel.write_result(case.case_id + 1, resp.text, 'FAIL')
            raise e

    @classmethod
    def tearDownClass(cls):
        # 1.关闭需要关闭的内容
        cls.http_request.close()  # 关闭session对象，清除cookies
        cls.mysql.close()  # 关闭数据库连接