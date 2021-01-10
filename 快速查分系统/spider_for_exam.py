"""
爬取学校校务系统考试成绩

"""

from selenium import webdriver
from selenium.common.exceptions import *
import time
import re
import json


class Spider:

    def __init__(self, name, username, password):
        print('#' * 50)
        self.name = name
        self.username = username
        self.password = password
        self.url = 'http://my.qchm.edu.cn/cas/login'
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.__login()

    def __login(self):
        driver = self.driver
        driver.get(self.url)
        driver.find_element_by_name('username').send_keys(self.username)
        driver.find_element_by_name('password').send_keys(self.password)
        driver.find_element_by_id('dl').click()
        time.sleep(1)
        try:
            if driver.find_element_by_id('errormsg').text == '用户名或密码错误':
                print('!' * 25)
                print(self.name + "密码错误")
                print('!' * 25)
                return
        except NoSuchElementException as e:
            print('成功登陆')
            time.sleep(2)
            return self.__handle(driver)

    def __handle(self, driver):
        data = {}
        data['name'] = self.name
        data['num'] = self.username
        driver.get('http://221.215.177.211/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default')
        time.sleep(2)
        # res = driver.find_element_by_id('area_four').text
        driver.find_element_by_id('search_go').click()
        time.sleep(2)
        res = driver.find_element_by_id('tabGrid').text
        res = self.__str_handle(res)
        data['result'] = res
        print('=' * 25)
        print(data['result'])
        print('=' * 25)
        self.__save(data)
        print('#' * 50)

        driver.close()

    def __str_handle(self, res):
        sub = re.findall(' [0-9]{8} \S{4,9}', res)
        ach = re.findall(' 100 | [3-9][0-9] ', res)
        return dict(zip(sub, ach))

    def __save(self, res):
        with open('achievement.json', 'a+') as f:
            json.dump(res, f)
        print(self.name + '成绩保存完毕')
