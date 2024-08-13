from subprocess import check_call, CalledProcessError
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import chromedriver_autoinstaller as chromedriver
import time
import pickle

project_path = [
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/b2b/ecommerce-service-store-b2b", "release/1.0.X", '2.0.0'),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/osb/ecommerce-service-mall", "release/2.4.X", '2.0.1'),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/mkp/ecommerce-service-store-mkp", "release/2.4.X", '2.0.2'),
    ("/Users/aaron.tanhenkel.com/Documents/Project/Git/abc/ecommerce-service-mall", "release/3.0.X", '2.0.0'),
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
    # 使用Chrome浏览器的选项，以便能够复用现有的用户数据和登录状态
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument(
        '--user-data-dir=/Users/aaron.tanhenkel.com/Library/Application Support/Google/Chrome')
    chrome_options.add_argument('--profile-directory=Default')  # 可能需要更改 'Profile 1' 以匹配您的实际配置

    chrome_options.set_capability("unhandledPromptBehavior", "accept")

    return webdriver.Chrome(chromedriver.install(), chrome_options=chrome_options)


def createPR(wb, version):
    url = "https://dev.azure.com/henkeldx/RAQN%20DCP/_git/ecommerce-gateway-store-b2b/pullrequests?_a=mine"

    delay(1)
    # wb.get(url)
    wb.execute_script(f"window.open('{url}', '_blank')")

    # 切换到新打开的标签页
    wb.switch_to.window(wb.window_handles[-1])

    delay(2)
    # create a pull request
    button = wb.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div[2]/a')
    ActionChains(wb).move_to_element(button).click(button).perform()
    delay(3)

    # input title
    description = 'docs(): update version to ' + version + '-SNAPSHOT'
    title = wb.find_element_by_xpath(
        "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/input")
    title.send_keys(description)

    # choose target branch
    branch = wb.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/span/span[2]/div/button')
    ActionChains(wb).move_to_element(branch).click(branch).perform()


if __name__ == '__main__':
    wb = configEnv()
    for index, (path, releaseName, version) in enumerate(project_path):
        print("Start process index:" + str(index) + " " + path + " " + pr_release_name + " " + version)
        createPR(wb, version)

        # doShell('git merge --strategy-option=theirs develop', path)
        # doShell('git push origin ' + pr_release_name, path)

        print("End process index:" + str(index) + " " + path + " " + pr_release_name)
        print("\n")
    delay(1000)
