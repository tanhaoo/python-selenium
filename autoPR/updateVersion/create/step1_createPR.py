from subprocess import check_call, CalledProcessError
import time

project_path = [
    ("/Users/tanaa/Documents/Project/b2b/ecommerce-service-store-b2b", "release/1.0.X",
     'b2b-2.0.5-SNAPSHOT'),
    ("/Users/tanaa/Documents/Project/osb/ecommerce-service-store-osb", "release/2.4.X",
     'osb-3.0.5-SNAPSHOT'),
    ("/Users/tanaa/Documents/Project/abc/ecommerce-service-store-abc", "release/3.0.X",
     'abc-4.0.5-SNAPSHOT'),
    # ("/Users/aaron.tanhenkel.com/Documents/Project/Git/mkp/ecommerce-service-store-mkp", "release/2.4.X",
    #  'mkp-2.4.26-SNAPSHOT'),
]

pr_release_name = "feature/"

mvn_update_version = "mvn versions:set -DnewVersion="


def delay(sec):
    time.sleep(sec)


def doShell(shell, path):
    try:
        command = f'source ~/.zshrc && {shell}'
        check_call(['zsh', '-c', command], cwd=path)
    except CalledProcessError as e:
        print("Error:", e)


if __name__ == '__main__':
    for index, (path, releaseName, version) in enumerate(project_path):
        print("Start process index:" + str(index) + " " + path + " " + releaseName)

        doShell('git checkout develop', path)
        doShell('git pull origin develop', path)

        delay(2)

        doShell('git branch ' + pr_release_name + version, path)
        doShell('git checkout ' + pr_release_name + version, path)

        delay(1)

        print(mvn_update_version + version)
        doShell(mvn_update_version + version, path)

        delay(1)

        description = 'docs(): update version to ' + version
        doShell('git add .', path)
        doShell('git commit -m "' + description + '"', path)

        print("End process index:" + str(index) + " " + path + " " + releaseName)
        print("\n")
