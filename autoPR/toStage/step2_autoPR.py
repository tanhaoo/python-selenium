from subprocess import check_call, CalledProcessError
from telnetlib import EC

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import chromedriver_autoinstaller as chromedriver
import time
import pickle

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

pr_release_name = "publish/13"
date = "20241009"

project_path = [
    # ("/Users/tanaa/Documents/Project/b2b/ecommerce-service-store-b2b", "release/1.0.X",
    #  'ecommerce-service-store-b2b', 'b2b-1.0.40-SNAPSHOT'),
    # ("/Users/tanaa/Documents/Project/osb/ecommerce-service-store-osb", "release/2.4.X",
    #  'ecommerce-service-store-osb', 'osb-2.4.19-SNAPSHOT'),
    # ("/Users/tanaa/Documents/Project/abc/ecommerce-service-store-abc", "release/3.0.X",
    #  'ecommerce-service-store-abc', 'abc-3.0.37-SNAPSHOT'),
    #
    # ("/Users/tanaa/Documents/Project/ecommerce-core-promotion", "release/2.2.X",
    #  'ecommerce-core-promotion', '2.2.X'),
    ("/Users/tanaa/Documents/Project/dependency-promotion-rule-engine", "release/2.0.X",
     'dependency-promotion-rule-engine', '2.0.X'),
    # ("/Users/tanaa/Documents/Project/ecommerce-service-promotion", "release/2.2.X",
    #  'ecommerce-service-promotion', '2.2.X'),

    # ("/Users/tanaa/Documents/Project/mkp/ecommerce-service-store-mkp", "release/2.4.X",
    #  'ecommerce-service-store-mkp', 'mkp-2.4.25-SNAPSHOT'),
    #
    # ("/Users/tanaa/Documents/Project/b2b/ecommerce-gateway-store-b2b", "release/1.0.X",
    #  'ecommerce-gateway-store-b2b', 'b2b-1.0.X-SNAPSHOT'),
    # ("/Users/tanaa/Documents/Project/osb/ecommerce-gateway-store-osb", "release/2.3.X",
    #  'ecommerce-gateway-store-osb', 'osb-2.3.X-SNAPSHOT'),
    # ("/Users/tanaa/Documents/Project/mkp/ecommerce-gateway-store-mkp", "release/2.2.X",
    #  'ecommerce-gateway-store-mkp', 'mkp-2.2.X-SNAPSHOT'),
    # ("/Users/tanaa/Documents/Project/abc/ecommerce-gateway-store-abc", "release/2.2.X",
    #  'ecommerce-gateway-store-abc', 'abc-2.2.X-SNAPSHOT'),
]


def delay(sec):
    time.sleep(sec)


def doShell(shell, path):
    try:
        check_call(shell, cwd=path, shell=True)
    except CalledProcessError as e:
        print("Error:", e)


def configEnv():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-data-dir=/Users/tanaa/Library/Application Support/Google/Chrome')

    # service = Service(ChromeDriverManager().install(), options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.101").install()),
                              options=chrome_options)
    return driver


def createPR(wb, serviceName, version, index):
    url = "https://dev.azure.com/henkeldx/RAQN%20DCP/_git/" + serviceName + "/pullrequestcreate?sourceRef=" + pr_release_name + "&targetRef=main"

    delay(1)
    # wb.get(url)
    wb.execute_script(f"window.open('{url}', '_blank')")

    # 切换到新打开的标签页
    wb.switch_to.window(wb.window_handles[-1])

    if index == 0:
        user_input = input("Enter your choice: ").strip().upper()

    delay(2)
    # input title
    title = wb.find_element(By.XPATH,
                            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/input")
    # 使用 JavaScript 清除输入框中的值
    # wb.execute_script("arguments[0].value = '';", title)
    # title.send_keys('release stage-' + version + '_' + date)
    title.click()
    # 手动选择所有文本并删除
    title.send_keys(Keys.HOME)  # 移动到文本的开头
    title.send_keys(Keys.SHIFT, Keys.END)  # 选择所有文本
    title.send_keys(Keys.DELETE)  # 删除选择的文本
    delay(1)
    title.send_keys('release stage-' + version + '_' + date)

    # create PR
    pr = wb.find_element(By.XPATH,
                         '//*[@id="skip-to-main-content"]/div/div[3]/div/div/div/div[6]/div/button')
    ActionChains(wb).move_to_element(pr).click(pr).perform()
    delay(10)

    auto = wb.find_element(By.XPATH, '//*[@id="skip-to-main-content"]/div/div[1]/div/div[1]/div[3]/button')
    ActionChains(wb).move_to_element(auto).click(auto).perform()
    delay(1)
    custom = wb.find_element(By.XPATH,
                             '//*[@id="__bolt-panel-1"]/div[2]/div/div[3]/div/div[3]/div[3]/div[1]/span/span')
    ActionChains(wb).move_to_element(custom).click(custom).perform()
    delay(1)
    commit_message = wb.find_element(By.XPATH,
                                     '/html/body/div[2]/div/div/div/div[2]/div/div[3]/div/div[3]/div[4]/div/div/input')
    commit_message.click()
    # 手动选择所有文本并删除
    commit_message.send_keys(Keys.HOME)  # 移动到文本的开头
    commit_message.send_keys(Keys.SHIFT, Keys.END)  # 选择所有文本
    commit_message.send_keys(Keys.DELETE)  # 删除选择的文本
    delay(1)
    commit_message.send_keys('release stage-' + version + '_' + date)

    set = wb.find_element(By.XPATH, '//*[@id="__bolt-complete"]')
    ActionChains(wb).move_to_element(set).click(set).perform()

if __name__ == '__main__':
    wb = configEnv()
    for index, (path, releaseName, serviceName, version) in enumerate(project_path):
        print("Start process index:" + str(index) + " " + path + " " + pr_release_name + " " + serviceName)

        doShell('git push origin ' + pr_release_name, path)
        delay(1)

        try:
            createPR(wb, serviceName, version, index)
        except NoSuchElementException as e:
            print("Error:", e)

        print("End process index:" + str(index) + " " + path + " " + pr_release_name)
        print("\n")
    delay(10000)
