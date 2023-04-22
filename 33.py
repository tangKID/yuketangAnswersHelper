import os
import json
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
url = 'https://changjiang.yuketang.cn'
global driver

def getCookies():
    driver = webdriver.Chrome()
    driver.get(url)
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'tab-student')))
    cookies = driver.get_cookies()
    f1 = open("cookies.txt", "w")
    f1.write(json.dumps(cookies))
    f1.close()
    driver.close()


def getIntoClass():
    now_time = time.strftime("%H:%M", time.localtime())
    driver = webdriver.Chrome()
    driver.get(url)
    f2 = open("cookies.txt")
    cookies = json.loads(f2.read())
    for cook in cookies:
        driver.add_cookie(cook)
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tab-student')))
    driver.find_element(By.ID, "tab-student").click()
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'tipbar')))
        driver.find_element(By.CLASS_NAME, "tipbar").click()
        driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/div[2]/div/div[2]').click()
        print(now_time, "bot:我去上课啦")
        print("我将会每10s检测一次有没有随堂测试")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        while True:
            time.sleep(10)
            answer(driver)
            # isClassOver(driver, now_time)
    except TimeoutException:
        print(now_time, "你现在没课")
        driver.close()


def autoRun():
    scheduler = BlockingScheduler(timezone='Asia/Beijing')
    scheduler.add_job(getIntoClass, 'cron', hour='6-22', minute='58', max_instances=20)
    scheduler.start()


def savePage(driver):
    f = open("savePage.html", 'wb')
    f.write(driver.page_source.encode("utf-8", "ignore"))
    print('写入成功')
    f.close()


def answer(driver):
    try:

        chooseB = driver.find_element(By.XPATH, '//p[@data-option="B"]')
        chooseB.click()
        submit = driver.find_element(By.XPATH, '//div[@style="width: 123.5px; min-height: 34.4px; left: 701px; top: 488.35px;"]')
        submit.click()
        print(time.strftime("%H:%M:%S", time.localtime()), "bot:我完成了一道题")
        driver.refresh()
    except NoSuchElementException:
        try:

            button = driver.find_element(By.XPATH, '//div[@style="width: 123.5px; min-height: 34.4px; left: 701px; top: 488.35px;"]')
            button.click()
            blank = driver.find_element(By.XPATH, '//textarea[@placeholder="输入答案"]')
            blank.click()
            blank.send_keys('不知道')
            block = driver.find_element(By.XPATH, '//p[@data-v-d9421cb0]')
            block.click()

            print(time.strftime("%H:%M:%S", time.localtime()), "bot:我完成了一道题")

            driver.refresh()
        except NoSuchElementException:
            driver.refresh()

def isClassOver(driver, now_time):
    tag = driver.find_element(By.ID, "value")
    if len(tag) != 0:
        driver.close()
        print(now_time, "bot:我回来啦")


if __name__ == "__main__":
    try:
        if os.path.exists("cookies.txt"):
            getIntoClass()
            autoRun()
        else:
            print("Hello，初次相遇需要先做一些设置，手动扫码登录一次，让我获取你的cookies。")
            getCookies()
            print("完成了, 现在我将在每个整点自动登录一次，如果发现有课就会进入教室上课。")
            print("挂在后台就好, 去做点真正有用的事情吧。\n")
            getIntoClass()
            autoRun()
    except Exception as ex:  # don't you ever stop!
        print(ex)
