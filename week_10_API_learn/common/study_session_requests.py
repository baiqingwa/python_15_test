# -*- coding: utf-8 -*-#
# Name:         study_session_requests
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/12 0012
"""
1,构造请求：请求方式，请求地址，请求参数
2，发起请求
3，返回响应
4，判断响应码，响应体

ip加端口号 域名 多个服务器 换一个环境 接口请求路径   判断：断言 cookie 用户信息
requests接口传参：
cookies 传对象或者字典
参数headers:(content_type )另一种数据格式
auth:认证 鉴权 权限(普通用户和vip)
timeout:发送连接时超时或返回响应时超时 type
重定向
proxies设置代理
verify:https不想认证 等于flase
stream :网页html抓包:保存文件流 抓包速度快
cert:传证书 证书浏览器下载到本地 或者找开发
"""

"""
两种传递cookie的方式
1，单独的session，把上一个请求的返回cookies，指定传递到下一个请求的入参cookie当中
2，使用同一个session，就会自动传递cookie。
cookies共享，session对象还在，代表它存在的时间 一定记得关闭
资源占用 关闭session
内存泄漏
"""
import requests
from week_10_API_learn.common.config import cf

class HTTPRequest:
    """
    独立session，cookies需要自己传递
    使用这类的request方法去完成不同的HTTP请求，并且返回响应结果
    """
    def request(self, method, url, data=None, json=None, cookies=None):

        method = method.upper()  # 将method强制转成全大小

        if type(data) == str:
            data = eval(data)  # str转成字典

        #数据处理
        if method == 'GET':
            # 请求结果异常处理
            try:
                resp = requests.get(url, params=data, cookies=cookies)  # resp 是Response对象
            except Exception as e:
                print('get请求出错：{}'.format(e))
        elif method == 'POST':
            try:
                if json:
                    resp = requests.post(url, json=json, cookies=cookies)
                else:
                    resp = requests.post(url, data=data, cookies=cookies)
            except Exception as e:
                print('post请求出错：{}'.format(e))
        else:
            resp = None
            print('UN-support method')

        return resp
# if __name__ == '__main__':

    # # 登录
    # params = {"mobilephone": "15810447878", "pwd": "123456"}
    # resp=HTTPRequest().request(method='POST',url='http://test.lemonban.com/futureloan/mvc/api/member/login',data=params)
    # print("响应码:", resp.status_code)
    # print("响应文本:", resp.text)
    # print("响应cookies:", resp.cookies)
    # print("请求cookies:", resp.request._cookies)
    # print("请求method:", resp.request.method)
    #
    # # 充值
    # params = {"mobilephone": "15810447878", "amount": "1000"}
    # resp2=HTTPRequest().request(method='POST',url='http://test.lemonban.com/futureloan/mvc/api/member/recharge',data=params,cookies=resp.cookies)
    # print("响应码:", resp2.status_code)
    # print("响应文本:", resp2.text)
    # print("响应cookies:", resp2.cookies)
    # print("请求cookies:", resp2.request._cookies)
    # print("请求method:", resp2.request.method)

    # 添加标的
    # params = {"memberId": "274", "title": "白庆买房记", "amount": "2000", "loanRate": "24.0", "loanTerm": "6","loanDateType": "0", "repaymemtWay": "4", "biddingDays": "8"}
    # requests3 = HTTPRequest().request(method='post', url='http://test.lemonban.com/futureloan/mvc/api/loan/add',data=params)
    # print(requests3.text)


class HttpRequest_session:
    """
    公共使用一个session, cookies自动传递
    使用这类的request方法去完成不同的HTTP请求，并且返回响应结果
    """
    def __init__(self):
        self.session=requests.sessions.session()

    def request(self,method,url,data=None,json=None):

        method = method.upper()#强制转换成大写

        if type(data) is str:
            data=eval(data) #转换成字典

        # 拼接URL（换环境）
        url = cf.get_values('api', 'server') + url

        if method == 'GET':
            try:
                resp = self.session.request(method=method,url=url,params=data)
            except Exception as e:
                print('get请求出错：{}'.format(e))
        elif method == 'POST':
            try:
                if json:
                    resp = self.session.request(method=method, url=url, json=json)
                else:
                    resp = self.session.request(method=method, url=url, data=data)
            except Exception as e:
                print('post请求出错：{}'.format(e))
        else:
            print('请求方法不存在')
        return resp

    def close(self):
        self.session.close()   # 用完记得关闭，很关键！！！
        return None
if __name__ == '__main__':
    session_request = HttpRequest_session()
    # 注册
    # params={"mobilephone": "15703033005", "pwd":'123456'}
    # resp=session_request.request(method='post',url='http://test.lemonban.com/futureloan/mvc/api/member/register',data=params)
    # print(resp.headers)
    # 登录
    params = {"mobilephone": "15703033005", "pwd":'123456'}
    requests=session_request.request(method='POST',url='http://test.lemonban.com/futureloan/mvc/api/member/login',data=params)
    print(requests.text)
    # print(requests.status_code)
    # print(requests.headers)
    # print(requests.status_code)
    # print(requests.cookies)
    # 充值
    # params = {"mobilephone": "15703033005", "amount": "1000"}
    # requests2=session_request.request(method='POST',url='http://test.lemonban.com/futureloan/mvc/api/member/recharge',data=params)
    # print(requests2.text)
    # print(requests2.headers)
    # print(requests2.status_code)
    # print(requests2.cookies)
    # session_request.close()  #重要
    # #添加标的
    params={"memberId":"(274)","title":"白庆买房记","amount":"999.9","loanRate":"26.0","loanTerm":"6","loanDateType":"8","repaymemtWay":"4","biddingDays":"8"}
    requests3=session_request.request(method='post',url='http://test.lemonban.com/futureloan/mvc/api/loan/add',data=params)
    print(requests3.text)
    # 投资
    params={"memberId":"(274)","password":"123456","loanId":"894","amount":"10000000000"}

    requests3=session_request.request(method='post',url='http://test.lemonban.com/futureloan/mvc/api/member/bidLoan',data=params)
    print(requests3.text)

    #审核
    params={"id":"{912}","status":"7"}
    requests3 = session_request.request(method='post', url='http://test.lemonban.com/futureloan/mvc/api/loan/audit',data=params)
    print(requests3.text)



