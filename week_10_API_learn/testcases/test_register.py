# -*- coding: utf-8 -*-#
# Name:         register
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/16 0016
import unittest
from ddt import ddt, data  # 装饰器
from week_10_API_learn.common import study_session_requests
from week_10_API_learn.common.Do_excel import DoExcel
from week_10_API_learn.common.contents_ml import case_file
from week_10_API_learn.common.Mysql_data import Mysql


@ddt  # @ddt装饰测试类 unittest.TestCase的子类
class TestAdd(unittest.TestCase):
    '''自动化测试框架，完成接口自动化'''
    # 1.创建操作excel的实例化对象,拿到测试数据
    do_excel = DoExcel(case_file, 'register')
    cases = do_excel.get_cases()
    @classmethod
    def setUpClass(cls):
        # 1.创建所需对象，方便调用方法（request请求、数据库）
        cls.http_request = study_session_requests.HttpRequest_session()
        cls.Mysql=Mysql()

    @data(*cases)
    def test_register(self,case):
        #1.判断手机号数据参数化：
        if case.data.find('result_mobilephone') > -1:
        #2.替换参数值(查询数据库以最大手机号+1作为注册的手机号)
            global new_mobilephone
            new_mobilephone=int(self.Mysql.get_fetch_one('select max(mobilephone) from future.member')['max(mobilephone)']) + 1
            #方法1：替换
            #case.data=case.data.replace('result_mobilephone',str(new_mobilephone))
            #方法2：使用json转换格式 字典赋值
            import json
            case.data=json.loads(case.data)
            case.data['mobilephone']=new_mobilephone
        #3.接口请求
        resp = self.http_request.request(case.method, case.url, case.data)
        actual=resp.text

        #4.断言结果
        try:
            self.assertEqual(case.expected, actual)
            print(actual)
            self.do_excel.write_result(case.case_id + 1, actual, 'PASS')
            # 5.进行参数校验(判断数据库是否存在注册成功后的手机号)
            # new_mobilephone = 15703033005  # 数据库最大手机号+1 被注册到最大 所以这里用已注册的一个手机号代替数据的验证
            if resp.json()['msg'] == '注册成功':
                sql = 'select mobilephone from future.member where mobilephone={}'.format(str(new_mobilephone))
                mobilephone = self.Mysql.get_fetch_one(sql)['mobilephone']
                try:
                    self.assertEqual(new_mobilephone, int(mobilephone))
                except Exception as e:
                    print('验证失败，错误：{}，数据库没有对应的数据'.format(e))
        except AssertionError as e:
            self.do_excel.write_result(case.case_id + 1, actual, 'FAIL')
            raise e

    @classmethod
    def tearDownClass(cls):
        # 1.关闭需要关闭的内容
        cls.http_request.close()  # 关闭session对象，清除cookies
        cls.mysql.close()  # 关闭数据库连接
