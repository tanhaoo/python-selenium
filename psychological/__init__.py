import time

import requests
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

count = 0


def delay(sec):
    time.sleep(sec)


def getSubject():
    # 针对多个class Name情况
    global count
    count += 1
    subject = wb.find_element_by_xpath(
        '/html/body/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[1]/section/div/div[1]/div[2]/span')
    answers = wb.find_elements_by_css_selector('.optionsItems.active')
    subject_text = str(count) + " " + subject.text
    print(subject_text)
    fp.write(subject_text + '\n')
    for result in answers:
        answer = result.find_element_by_class_name('optionsTitle')
        answer_text = answer.text
        print(answer_text)
        fp.write(answer_text + '\n')
    fp.write('\n')

    button = wb.find_element_by_xpath(
        '/html/body/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[2]')
    ActionChains(wb).move_to_element(button).click(button).perform()


if __name__ == '__main__':
    url = "http://www.siyuanren.com/startExam/chaptExamList/?packId=388&packName=%E5%BF%83%E7%90%86%E5%92%A8%E8%AF%A2%E5%B8%88%E5%9F%BA%E7%A1%80%E5%9F%B9%E8%AE%AD%E9%A1%B9%E7%9B%AE2.0"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    chrome_driver = "/usr/local/bin/chromedriver"

    wb = webdriver.Chrome(executable_path=chrome_driver)
    wb.get(url)
    a = input("等待输入验证码")

    second_url = "http://www.siyuanren.com/startExam/chaptExamList?packId=388&packName=%E5%BF%83%E7%90%86%E5%92%A8%E8%AF%A2%E5%B8%88%E5%9F%BA%E7%A1%80%E5%9F%B9%E8%AE%AD%E9%A1%B9%E7%9B%AE2.0"
    wb.get(second_url)
    # 背题模式
    wb.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[2]').click()
    # 开始做题
    delay(0.8)
    # 理论知识
    # wb.find_element_by_xpath(
    #     '/html/body/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[3]/div').click()
    # 操作技能
    wb.find_element_by_xpath(
        '/html/body/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div').click()
    fp = open("Psychological Subject.txt", "w", encoding='utf-8')
    for page in range(23):
        delay(1)
        for i in range(20):
            getSubject()
        confirm = wb.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div[3]/div/div/ul/div/div[2]')
        ActionChains(wb).move_to_element(confirm).click(confirm).perform()
