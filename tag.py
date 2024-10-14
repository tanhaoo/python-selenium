import os
import subprocess
import shutil
import time
git = os.environ.get('GIT', "git")

script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dir_repos = "repositories"


tag_list = {
#     "abc":"v3.0.38",
    "mkp":"v2.4.43",
    "osb":"v2.4.22",
    "back_office":"v2.53.240926",
    "b2b":"v1.0.39"
}
abc_group = {
    "ecommerce-gateway-store-abc": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-gateway-store-abc",
    "ecommerce-service-store-abc": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-store-abc",
    "ecommerce-service-integration-abc": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-integration-abc"
}


mkp_group = {
    "ecommerce-gateway-store-mkp": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-gateway-store-mkp",
    "ecommerce-service-store-mkp": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-store-mkp",
    "ecommerce-service-integration-mkp": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-integration-mkp"
}


osb_group = {
    "ecommerce-gateway-store-osb": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-gateway-store-osb",
    "ecommerce-service-store-osb": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-store-osb",
    "ecommerce-service-integration-osb": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-integration-osb"
}

b2b_group = {
    "ecommerce-gateway-store-b2b": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-gateway-store-b2b",
    "ecommerce-service-store-b2b": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-store-b2b",
    "ecommerce-service-integration-b2b": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-integration-b2b"
}

back_office_group = {
    "foundation-core-audit": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/foundation-core-audit",
    "foundation-backend-gateway":"git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/foundation-backend-gateway",
    "ecommerce-core-digitalasset":"git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-core-digitalasset",
    "ecommerce-service-domainjobs":"git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-domainjobs",
    "ecommerce-core-inventory":"git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-core-inventory",

    "foundation-core-masterdata": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/foundation-core-masterdata",
    "ecommerce-service-oms":"git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-oms",
    "ecommerce-core-order": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-core-order",
    "ecommerce-service-orderhub": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-orderhub",
    "ecommerce-core-payment": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-core-payment",
    "ecommerce-service-pim": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-pim",
    "ecommerce-core-product": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-core-product",
    "ecommerce-service-productsearch":"git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-productsearch",
    "dependency-promotion-rule-engine": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/dependency-promotion-rule-engine",
    "ecommerce-core-promotion": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-core-promotion",
    "ecommerce-service-promotion": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-promotion",
    "ecommerce-service-seller-api": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/ecommerce-service-seller-api",
    "foundation-core-task": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/foundation-core-task",
    "foundation-core-user": "git@ssh.dev.azure.com:v3/henkeldx/RAQN%20DCP/foundation-core-user"
}






def git_clone_tag(url, dir, name, tag_version):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        print('del dir %s ok' %dir)

    run(f'"{git}" clone "{url}" "{dir}"', f"Cloning {name} into {dir}...", f"Couldn't clone {name}")

    tag = run(f'"{git}" -C "{dir}" tag -l {tag_version}', None, None).strip()
    run(f'"{git}" -C "{dir}" checkout main', None, None)
    if(len(tag) == 0):
        run(f'"{git}" -C "{dir}" tag -a {tag_version} -m "Automatically created by Python scripts."', f"create {name} tag: {tag_version} ...", None)
        run(f'"{git}" -C "{dir}" push origin {tag_version}', f"push {name} tag: {tag_version} ...", None)
    else:
        print('tag %s exist, ignore...' %tag_version)

def del_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path)
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_lis = os.listdir(dir_path)
        for file_name in file_lis:
            # if file_name != 'wibot.log':
            tf = os.path.join(dir_path, file_name)
            del_files(tf)
    print('del dir %s ok' %dir_path)


def run(command, desc=None, errdesc=None, custom_env=None, live=False):
    if desc is not None:
        print(desc)

    if live:
        result = subprocess.run(command, shell=True, env=os.environ if custom_env is None else custom_env)
        if result.returncode != 0:
            raise RuntimeError(f"""{errdesc or 'Error running command'}.
            Command: {command}
            Error code: {result.returncode}""")

        return ""

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ if custom_env is None else custom_env)

    if result.returncode != 0:

        message = f"""{errdesc or 'Error running command'}.
            Command: {command}
            Error code: {result.returncode}
            stdout: {result.stdout.decode(encoding="utf8", errors="ignore") if len(result.stdout)>0 else '<empty>'}
            stderr: {result.stderr.decode(encoding="utf8", errors="ignore") if len(result.stderr)>0 else '<empty>'}
            """
        raise RuntimeError(message)

    return result.stdout.decode(encoding="utf8", errors="ignore")

def repo_dir(name):
    return os.path.join(script_path, dir_repos, name)



def abc():
    if 'abc' not in tag_list:
        print("abc no tag version, ignore ..........")
        return
    tag_version = tag_list.get("abc")
    for name, url in abc_group.items():
        git_clone_tag(url, repo_dir(name), name, tag_version)


def mkp():
    if 'mkp' not in tag_list:
        print("mkp no tag version, ignore ..........")
        return
    tag_version = tag_list.get("mkp");
    for name, url in mkp_group.items():
        git_clone_tag(url, repo_dir(name), name, tag_version)


def osb():
    if 'osb' not in tag_list:
        print("osb no tag version, ignore ..........")
        return
    tag_version = tag_list.get("osb");
    for name, url in osb_group.items():
        git_clone_tag(url, repo_dir(name), name, tag_version)

def b2b():
    if 'b2b' not in tag_list:
        print("b2b no tag version, ignore ..........")
        return
    tag_version = tag_list.get("b2b");
    for name, url in b2b_group.items():
        git_clone_tag(url, repo_dir(name), name, tag_version)

def back_office():
    if 'back_office' not in tag_list:
        print("back_office no tag version, ignore ..........")
        return
    tag_version = tag_list.get("back_office");
    for name, url in back_office_group.items():
        git_clone_tag(url, repo_dir(name), name, tag_version)

def test():
    for name, url in back_office_group.items():
        msg = name + ' digitalasset-domain-jar ' + url
        print("sh /Users/yunpeng.kong/scripts/build.sh %s" %msg)

def start():
    abc()
    mkp()
    osb()
    b2b()
    back_office()

if __name__ == "__main__":
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    start()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))