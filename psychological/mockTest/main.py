import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

count = 0


def delay(sec):
    time.sleep(sec)


def getExamUrl(id):
    return "http://www.siyuanren.com/startExam/historyExamPage?examId=" + str(id) + "&type=1"


def getExamUrls(urls):
    # Exam ID 很随机
    for i in range(540, 550):
        urls.append(getExamUrl(i))
    for j in range(459, 463):
        urls.append(getExamUrl(j))
    urls.append(getExamUrl(465))
    urls.append(getExamUrl(464))
    urls.append(getExamUrl(468))
    urls.append(getExamUrl(469))
    urls.append(getExamUrl(494))
    urls.append(getExamUrl(700))


def getSubject():
    # 针对多个class Name情况
    global count
    count += 1
    subject = wb.find_element_by_xpath(
        '/html/body/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/section/div/div[1]/div[2]/span')
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

    next_button = wb.find_element_by_xpath(
        '/html/body/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/div[2]')
    ActionChains(wb).move_to_element(next_button).click(next_button).perform()


if __name__ == '__main__':
    exam_urls = []

    url = "http://www.siyuanren.com/startExam/chaptExamList/?packId=388&packName=%E5%BF%83%E7%90%86%E5%92%A8%E8%AF%A2%E5%B8%88%E5%9F%BA%E7%A1%80%E5%9F%B9%E8%AE%AD%E9%A1%B9%E7%9B%AE2.0"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    chrome_driver = "/usr/local/bin/chromedriver"

    getExamUrls(exam_urls)
    for index, exam_url in enumerate(exam_urls):
        print(str(index) + ":" + exam_url)
    wb = webdriver.Chrome(executable_path=chrome_driver)
    wb.get(url)
    a = input("等待输入验证码")
    fp = open("MockExam.txt", "w", encoding='utf-8')

    for index, exam_url in enumerate(exam_urls):
        wb.get(exam_url)
        # 开始做题
        delay(1)
        for i in range(500):
            getSubject()
            try:
                if wb.find_element_by_css_selector('.nextBtn.info') is not None:
                    break
            except NoSuchElementException:
                print()
