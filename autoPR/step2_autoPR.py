from subprocess import check_call, CalledProcessError
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import chromedriver_autoinstaller as chromedriver
import time
import pickle

project_path = [
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/b2b/ecommerce-gateway-store-b2b", "release/1.0.X"),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/b2b/ecommerce-service-store-b2b", "release/1.0.X"),

    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/osb/ecommerce-gateway-store-osb", "release/2.3.X"),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/osb/ecommerce-service-mall", "release/2.4.X"),

    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/mkp/ecommerce-service-store-mkp", "release/2.4.X"),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/mkp/ecommerce-gateway-store-mkp", "release/2.2.X"),

    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/abc/ecommerce-gateway-store-abc", "release/2.2.X"),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/abc/ecommerce-service-mall", "release/3.0.X"),
]

pr_release_name = "feature/security"


def delay(sec):
    time.sleep(sec)


def doShell(shell, path):
    try:
        check_call(shell, cwd=path, shell=True)
    except CalledProcessError as e:
        print("Error:", e)


def configEnv():
    url = "https://dev.azure.com/henkeldx/RAQN%20DCP/_git/ecommerce-gateway-store-b2b/pullrequests?_a=mine"
    # 使用Chrome浏览器的选项，以便能够复用现有的用户数据和登录状态
    chrome_options = webdriver.ChromeOptions()

    # # GPU硬件加速
    # chrome_options.add_argument('–-disable-gpu')
    # # 彻底停用沙箱
    # chrome_options.add_argument('--no-sandbox')
    # # 创建临时文件共享内存
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # # 单进程运行
    # chrome_options.add_argument('-–single-process')

    chrome_options.add_argument(
        '--user-data-dir=/Users/aaron.tanhenkel.com/Library/Application Support/Google/Chrome')
    chrome_options.add_argument('--profile-directory=Default')  # 可能需要更改 'Profile 1' 以匹配您的实际配置

    wb = webdriver.Chrome(chromedriver.install(), chrome_options=chrome_options)
    wb.get(url)

    # create a pull request
    button = wb.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div[2]/a')
    ActionChains(wb).move_to_element(button).click(button).perform()
    delay(1)

    # input title
    title = 'docs(): update version to 2.4.23-SNAPSHOT'

    # choose target branch
    branch = wb.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/span/span[2]/div/button')
    ActionChains(wb).move_to_element(branch).click(branch).perform()
    delay(10)


if __name__ == '__main__':
    configEnv()
    delay(1000)
    # for index, (path, releaseName) in enumerate(project_path):
    #     print("Start process index:" + str(index) + " " + path + " " + pr_release_name)
    #
    #     doShell('git merge --strategy-option=theirs develop', path)
    #     doShell('git push origin ' + pr_release_name, path)
    #
    #     print("End process index:" + str(index) + " " + path + " " + pr_release_name)
    #     print("\n")
