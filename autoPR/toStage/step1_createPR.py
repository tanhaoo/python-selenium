from subprocess import check_call, CalledProcessError
import time

project_path = [
    # ("/Users/tanaa/Documents/Project/b2b/ecommerce-gateway-store-b2b", "release/1.0.X"),
    # ("/Users/tanaa/Documents/Project/osb/ecommerce-gateway-store-osb", "release/2.3.X"),
    # ("/Users/tanaa/Documents/Project/mkp/ecommerce-gateway-store-mkp", "release/2.2.X"),
    # ("/Users/tanaa/Documents/Project/abc/ecommerce-gateway-store-abc", "release/2.2.X"),

    # ("/Users/tanaa/Documents/Project/Git/mkp/ecommerce-service-store-mkp", "release/2.4.X"),
    ("/Users/tanaa/Documents/Project/b2b/ecommerce-service-store-b2b", "release/1.0.X"),
    ("/Users/tanaa/Documents/Project/osb/ecommerce-service-store-osb", "release/2.4.X"),
    ("/Users/tanaa/Documents/Project/abc/ecommerce-service-store-abc", "release/3.0.X"),
    #
    ("/Users/tanaa/Documents/Project/ecommerce-core-promotion", "release/2.2.X"),
    ("/Users/tanaa/Documents/Project/dependency-promotion-rule-engine", "release/2.0.X"),

    # ("/Users/tanaa/Documents/Project/ecommerce-service-promotion", "release/2.2.X"),

]

pr_release_name = "publish/20"


def delay(sec):
    time.sleep(sec)


def doShell(shell, path):
    try:
        check_call(shell, cwd=path, shell=True)
    except CalledProcessError as e:
        print("Error:", e)


if __name__ == '__main__':
    for index, (path, releaseName) in enumerate(project_path):
        print("Start process index:" + str(index) + " " + path + " " + releaseName)

        doShell('git checkout ' + releaseName, path)
        doShell('git pull origin ' + releaseName, path)

        delay(1)

        doShell('git checkout main', path)
        doShell('git pull origin main', path)

        delay(1)

        doShell('git branch ' + pr_release_name, path)
        doShell('git checkout ' + pr_release_name, path)

        doShell('git merge --strategy-option=theirs ' + releaseName, path)
        # doShell('git push origin ' + pr_release_name, path)

        print("End process index:" + str(index) + " " + path + " " + releaseName)
        print("\n")
