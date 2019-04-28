# -*- coding: utf-8 -*-#
# Name:         Mysql
# Author:       白庆
# Email：       364164232@qq.com
# Time:         2019/4/19 0019

#需安装
import pymysql
from week_10_API_learn.common.config import cf

class Mysql:
    def __init__(self):
        self.host=cf.get_values('mysql','host')
        self.port=cf.get_getint('mysql','port')
        self.user=cf.get_values('mysql','user')
        self.password=cf.get_values('mysql','password')
        #1.创建连接
        self.mysql=pymysql.connect(port=self.port,host=self.host,user=self.user,password=self.password)
        #2.创建查询页面 游标 返回字典类型
        self.cursor=self.mysql.cursor(pymysql.cursors.DictCursor)
        #3.编写SQL语句
    def get_fetch_one(self,sql): #元祖
        #4.执行sql语句
        self.cursor.execute(sql)
        #     #提交sql语句，完成数据库数据更新
        self.mysql.commit()
        #5.返回结果 查询结果集 最近的一条数据返回
        return self.cursor.fetchone()

    def get_fetch_all(self,sql):
        #4.执行sql语句
        self.cursor.execute(sql)
        self.mysql.commit()
        #5.返回结果 获取全部结果集 元祖粗存
        return self.cursor.fetchall()

    def close_cursor_mysql(self):
        #6.关闭游标
        self.cursor.close()
        #7.关闭数据库连接
        self.mysql.close()
if __name__ == '__main__':
    mysql=Mysql()
    m=mysql.get_fetch_all('select mobilephone from future.member limit 10')
    mysql.close_cursor_mysql()
    print(m)
