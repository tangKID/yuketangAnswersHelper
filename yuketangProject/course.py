# -*- coding: utf-8 -*-
"""
1.首先设置时必须要写手机号，然后要在旧版中设置密码
"""
from selenium.common.exceptions import NoSuchElementException
import time
from utils import input_selected_course_id, input_course_id, input_stu_card_id


class StuCourse:

    # 初始化必要参数
    def __init__(self, login_browser):
        self.browser = login_browser

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
                selected_course_id = input_course_id(course_count)
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
            index_of_selected_handle = input_selected_course_id(index_of_selected_course_handle,
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
            selected_stu_card_id = input_stu_card_id(index_of_stu_card)
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