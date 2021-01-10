# -*- coding: utf-8 -*-
"""
PS:首先声明：本脚本只做学习交流的用途，严禁用于任何商业非法用途，产生后果由使用脚本的人负责
@author : tangKID
目前完成的功能如下:
    1.自动登录
    2.自动签到
    3.自动预习ppt
"""
from urllib import request
from urllib.parse import quote
import string
import time
from login import StuLogin

PUSH_KEY = 'SCU133471Ta944ad257e323bde52041ac0a73337055fce565b7d6d8'
times = 1


# 服务器监控, 这个借助了自动化脚本大佬的思路，算是二次迭代，顺便了解了Server酱
def server_monitor(refresh_rate, task):
    count = 0
    while True:
        count += 1
        if count > times:
            msg = 'NotFoundOnlineClass'
            print('https://sc.ftqq.com/' + PUSH_KEY + '.send?text=' + msg)
            request.urlopen('https://sc.ftqq.com/' + PUSH_KEY + '.send?text=' + msg)
            print(msg)
            break

        result = task.sign_online_class()
        if result[0]:
            msg = 'AttendSuccess'
            url = quote('https://sc.ftqq.com/' + PUSH_KEY + '.send?text=' + msg + '&desp=' + result[1],
                        safe=string.printable)
            request.urlopen(url)
            print(msg + ' CourseName: ' + result[1])

            break
        print('The ' + str(count) + ' times did not success')
        time.sleep(refresh_rate * 10)


if __name__ == '__main__':
    stu_username = '13955114261'  # 必须是手机号
    stu_password = 'Kid11111111'  # 绑定手机号的密码
    CHROME_DRIVER = r"E:\chromedriver.exe"  # 需要自己下载驱动
    task = StuLogin(CHROME_DRIVER, stu_username, stu_password)
    print('开启浏览器')
    task.setBrowser()
    task.login()
    print('自动登录.....')
    server_monitor(1, task)