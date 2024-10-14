from platform import version
from subprocess import check_call, CalledProcessError
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller as chromedriver
import time
import pickle

from selenium.webdriver.common.keys import Keys

project_path = [
    ("/Users/tanaa/Documents/Project/b2b/ecommerce-service-store-b2b", "release/1.0.X",
     'ecommerce-service-store-b2b', 'b2b-1.0.39-SNAPSHOT', "release-1.0.X"),
    # ("/Users/aaron.tanhenkel.com/Documents/Project/Git/osb/ecommerce-service-mall", "release/2.4.X",
    #  'ecommerce-service-store-osb', 'osb-2.4.18-SNAPSHOT'),
    # ("/Users/aaron.tanhenkel.com/Documents/Project/Git/abc/ecommerce-service-mall", "release/3.0.X",
    #  'ecommerce-service-store-abc', 'abc-3.0.35-SNAPSHOT'),
    # ("/Users/aaron.tanhenkel.com/Documents/Project/Git/mkp/ecommerce-service-store-mkp", "release/2.4.X",
    #  'ecommerce-service-store-mkp', 'mkp-2.4.26-SNAPSHOT'),
]

pr_release_name = "feature/"


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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.59").install()),
                              options=chrome_options)
    return driver


def createPR(wb, serviceName, version):
    url = "https://dev.azure.com/henkeldx/RAQN%20DCP/_git/" + serviceName + "/pullrequestcreate?sourceRef=" + pr_release_name + version + "&targetRef=develop"

    # wb.get(url)
    wb.execute_script(f"window.open('{url}', '_blank')")
    print(url)
    # 切换到新打开的标签页
    wb.switch_to.window(wb.window_handles[-1])

    if index == 0:
        user_input = input("Enter your choice: ").strip().upper()

    # # input title
    # title = wb.find_element(By.XPATH,
    #                         "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/input")
    # # 使用 JavaScript 清除输入框中的值
    # wb.execute_script("arguments[0].value = '';", title)
    # delay(2)
    # title.send_keys('docs(): update version to ' + version)
    common(version, wb)

    set = wb.find_element(By.XPATH, '//*[@id="__bolt-complete"]')
    ActionChains(wb).move_to_element(set).click(set).perform()

    delay(1)
    # '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div[3]/div/div[2]'
    work_items = wb.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div[3]/div/div[2]')
    work_items.click()
    delay(2)
    actions = ActionChains(wb)
    actions.send_keys(Keys.COMMAND, 'v')  # Mac 使用 COMMAND, Windows/Linux 使用 CONTROL
    delay(2)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    # work_items.click()
    # delay(2)
    # work_items.send_keys(Keys.CONTROL, 'v')
    # delay(2)
    # work_items.send_keys(Keys.ENTER)
    # wb.execute_script("arguments[0].value = '" + "510226" + "';", work_items)

def cherryPR(wb, serviceName, version, releaseName, urlPrefix):
    url = "https://dev.azure.com/henkeldx/RAQN%20DCP/_git/" + serviceName + "/pullrequestcreate?sourceRef=" + pr_release_name + version + "-on-" + urlPrefix + "&targetRef=" + releaseName
    wb.execute_script(f"window.open('{url}', '_blank')")
    print(url)
    # 切换到新打开的标签页
    wb.switch_to.window(wb.window_handles[-1])
    common(version, wb)


def common(version, wb):
    delay(2)
    # create PR
    pr = wb.find_element(By.XPATH,
                         '//*[@id="skip-to-main-content"]/div/div[3]/div/div/div/div[6]/div/button')
    ActionChains(wb).move_to_element(pr).click(pr).perform()
    delay(3)
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
    commit_message.send_keys('docs(): update version to ' + version)


if __name__ == '__main__':
    wb = configEnv()
    for index, (path, releaseName, serviceName, version, urlPrefix) in enumerate(project_path):
        print("Start process index:" + str(index) + " " + path + " " + pr_release_name + version + " " + serviceName)

        doShell('git push origin ' + pr_release_name + version, path)
        delay(1)
        try:
            createPR(wb, serviceName, version)
            # cherryPR(wb, serviceName, version, releaseName, urlPrefix)
        except NoSuchElementException as e:
            print("Element not found:", e)

        print("End process index:" + str(index) + " " + path + " " + pr_release_name)
        print("\n")
    delay(100000)
