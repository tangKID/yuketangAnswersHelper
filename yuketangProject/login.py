# -*- coding: utf-8 -*-
"""
1.首先设置时必须要写手机号，然后要在旧版中设置密码
2.尽量不要开启代理服务器，因为这样会很慢，导致脚本获取不到数据
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import utils
import json
import time

from course import StuCourse


class StuLogin:
    browser = None
    __browser_driver = None
    __username = ''
    __password = ''

    # 初始化必要参数
    def __init__(self, browser_driver, stu_username, stu_password):
        self.__browser_driver = browser_driver
        self.__username = stu_username
        self.__password = stu_password

    # 设置浏览器的驱动并获得句柄
    def setBrowser(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(executable_path=self.__browser_driver, options=options)

    # 登录
    def login(self):
        url = 'https://changjiang.yuketang.cn/web'
        self.browser.get(url)
        self.browser.find_element_by_css_selector('.changeImg').click()
        input_elem = self.browser.find_element_by_css_selector('input[name=loginname]')
        pwd_elem = self.browser.find_element_by_css_selector('input[name=password]')
        input_elem.clear()
        pwd_elem.clear()
        input_elem.send_keys(self.__username)
        pwd_elem.send_keys(self.__password)
        pwd_elem.send_keys(Keys.ENTER)

    # 签到正在上网课的课程
    def sign_online_class(self):
        try:
            time.sleep(5)  # 从登录界面进来，必须要等待浏览器加载，否则获取不到数据
            flag = input("当前是否开始进行签到[y/n]:")
            if flag == 'y':

                # 2.开始签到
                self.browser.find_element_by_css_selector('.onlesson').click()
                time.sleep(2)
                self.browser.find_element_by_css_selector('.lessonlist').click()
                time.sleep(3)
                # 3.获取本节课的答案
                self.answer_of_this_course()

            else:
                # 4.登录页面后，选择tab页，选到"我听的课"
                tab_stu = self.browser.find_element_by_id('tab-student')
                if tab_stu.is_selected() is False:
                    tab_stu.click()
                # 5.进入课程列表，开始选择课程
                time.sleep(3)
                self.select_online_class()
            tmp = self.browser.title
            return [True, tmp]
        except NoSuchElementException:
            return [False]

    # 正在上课的课程答案
    def answer_of_this_course(self):
        try:
            self.browser.switch_to.window(self.browser.window_handles[-1])
            time.sleep(2)
            str_current_url = self.browser.current_url
            print(str_current_url)
            lesson_id = str_current_url.split('/')[5]
            print(lesson_id)
            answers_url = 'https://changjiang.yuketang.cn/v/lesson/get_lesson_replay_content/?lesson_id='+lesson_id
            print(answers_url)
            js = "window.open('" + answers_url + "');"
            self.browser.execute_script(js)
            self.browser.switch_to.window(self.browser.window_handles[-1])
            time.sleep(3)
            answers_str = self.browser.find_element_by_xpath('/html/body/pre').text
            # json数据处理
            data = json.loads(answers_str)
            problem_list_dict = data["data"]["problemList"]
            index_of_problem_list = []
            for i in range(0, len(problem_list_dict)):
                index = data["data"]["problemList"][i]["index"]
                index_of_problem_list.append(index)
            the_answers_dict = {}
            the_slides_list = data["data"]["presentationList"][0]["Slides"]
            for i in index_of_problem_list:
                the_temp_dict = the_slides_list[i-1]
                the_answer = the_temp_dict["Problem"]["Answer"]
                the_answers_dict[i] = the_answer
            if len(the_answers_dict) == 0:
                print("\n本节课无习题")
            else:
                print("\n本节课的答案:")
                print(the_answers_dict)
        except NoSuchElementException:
            print('未找到元素3')

    # 点开课程进行操作
    def select_online_class(self):
        course_name = {}
        try:
            course_count = len(self.browser.find_elements_by_css_selector('.studentCol')) + 1
            for i in range(1, course_count):
                each_course_name_xpath = '//*[@id="pane-student"]/div/div/div[' + str(i) + ']/div/div[1]/div/div[' \
                                                                                           '1]/div[1]/h1 '
                var = self.browser.find_element_by_xpath(each_course_name_xpath).text
                course_name[i] = var
                print('课程序号: ' + str(i) + ' |课程名称: ' + course_name[i])

            index_url = self.browser.current_url

            selected_course_handles_dict = {}
            index_of_selected_course_handle = -1
            while True:
                selected_course_id = utils.input_course_id(course_count)
                if selected_course_id == 0:
                    break
                if 0 < selected_course_id < course_count:
                    print('你选择了课程 :' + course_name[selected_course_id])

                    # 记录所选择课程所对应的，windows句柄
                    index_of_selected_course_handle += 1
                    selected_course_handles_dict[course_name[selected_course_id]] = index_of_selected_course_handle

                    selected_course_xpath = '//*[@id="pane-student"]/div/div/div[' + str(
                        selected_course_id) + ']/div'
                    self.browser.refresh()
                    time.sleep(5)
                    self.browser.find_element_by_xpath(selected_course_xpath).click()
                    print('第' + str(selected_course_id) + '个课程的页面url:' + self.browser.current_url)

                    time.sleep(2)
                    print('跳转到首页url:' + index_url)
                    js = "window.open('" + index_url + "');"
                    self.browser.execute_script(js)
                    time.sleep(3)
                    # 最后一个对象句柄是首页
                    self.browser.switch_to.window(self.browser.window_handles[-1])
                    time.sleep(2)
                    print('\n******如果不需要选择课程，请在下次输入时，输入0!******\n')

            print("请在所有选择的课程中，选择当前要查看的课程页面:")
            index_of_selected_handle = utils.input_selected_course_id(index_of_selected_course_handle,
                                                                      selected_course_handles_dict)
            self.browser.switch_to.window(self.browser.window_handles[index_of_selected_handle])
            time.sleep(3)

            # 需要把数据拉到底部，加载出新的数据
            js = "arguments[0].scrollIntoView();"
            stu_cards_name = {}
            index_of_stu_card = 1
            while True:
                each_stu_card_name_xpath = '//*[@id="pane--1"]/div[' + str(
                    index_of_stu_card) + ']/div/div[2]/div/h2'
                each_stu_card_category_xpath = '//*[@id="pane--1"]/div[' + str(index_of_stu_card) + ']/div/div[' \
                                                                                                    '1]/div/span[1] '
                var1 = self.browser.find_element_by_xpath(each_stu_card_name_xpath)
                var2 = self.browser.find_element_by_xpath(each_stu_card_category_xpath)
                stu_cards_name[index_of_stu_card] = {'课次名称': var1.text, '课次类别': var2.text}
                print(
                    '课次类别: ' + stu_cards_name[index_of_stu_card].get('课次类别') + '  |课次序号: ' + str(index_of_stu_card)
                    + '  |课次名称: ' + stu_cards_name[index_of_stu_card].get('课次名称'))
                self.browser.execute_script(js, var1)
                stu_card_count = len(self.browser.find_elements_by_xpath('//*[@id="pane--1"]/div'))
                if index_of_stu_card < stu_card_count:
                    index_of_stu_card += 1
                else:
                    break

            print("\n请在课程中，选择当前要查看的课次:\n")
            selected_stu_card_id = utils.input_stu_card_id(index_of_stu_card)
            selected_stu_card_xpath = '//*[@id="pane--1"]/div[' + str(selected_stu_card_id) + ']'

            var = self.browser.find_element_by_xpath(selected_stu_card_xpath)
            self.browser.execute_script(js, var)
            time.sleep(2)
            self.browser.find_element_by_xpath(selected_stu_card_xpath).click()
            # 自动化翻页ppt
            self.auto_ppt_play()
            print()
            self.browser.find_element_by_xpath('//*[@id="pane-student"]/div/div/div['+str(1)+']/div').click()
            self.browser.switch_to.window(self.browser.window_handles[1])

        except NoSuchElementException:
            print('未找到元素1')

    # 自动播放ppt(争对'课堂'的)(待修改)
    def auto_ppt_play(self):
        try:
            self.browser.refresh()
            time.sleep(3)

            if self.browser.find_element_by_xpath(
                    '//*[@id="app"]/div[2]/div/section/main/div[1]/div[1]/div/div/div['
                    '2]/div[2]/img') is not None:
                print('*************************1')

                self.browser.find_element_by_xpath(
                    '//*[@id="app"]/div[2]/div/section/main/div[1]/div[1]/div/div/div['
                    '2]/div[2]/img').click()
                time.sleep(3)
                ppt_pages = len(self.browser.find_elements_by_css_selector('.swiper-no-swiping'))
                ''''''
                for i in range(1, ppt_pages + 1):
                    self.browser.find_element_by_xpath(
                        '//*[@id="app"]/div[2]/div/section/main/div[1]/div[1]/div/div['
                        '2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div['
                        '' + str(i) + ']').click()
                    time.sleep(3)
            elif self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/section/main/div[1]/div[1]/div/div['
                                                    '2]/div[2]/img') is not None:
                print('*************************2')
                element1 = self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/section/main/div[1]/div['
                                                              '1]/div/div[ '
                                                              '2]/div[2]/img')
                self.browser.execute_script("arguments[0].click();", element1)
                time.sleep(3)
                ppt_pages = len(self.browser.find_elements_by_css_selector('.swiper-no-swiping'))
                for i in range(1, ppt_pages + 1):
                    self.browser.find_element_by_xpath(
                        '//*[@id="app"]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/div/'
                        'div[2]/div[1]/div[2]/div[1]/div[' + str(i) + ']').click()
                    time.sleep(10)
        except NoSuchElementException:
            print('未找到元素2')

