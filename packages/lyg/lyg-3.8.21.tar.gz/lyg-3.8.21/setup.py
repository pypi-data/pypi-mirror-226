import os
import distro
import shutil
from setuptools import setup, find_packages, Command
from setuptools.command.install import install

class CustomInstall(install):
    def do_egg_install(self):
        super().do_egg_install()
        self.run_post_install_tasks()

    def run_post_install_tasks(self):
        # 获取预期的包安装位置
        package_dir = os.path.join(self.install_lib, 'lyg')

        # 针对POSIX系统（Linux）的后处理
        if os.name == "posix":
            # 如果不是root用户，提示错误
            if os.getuid() != 0:
                raise PermissionError("You must run this with root privileges to install files in system directories.")
            
            # 对CentOS系统进行特殊处理
            linux_distro = distro.id()
            linux_version = distro.version()

            if linux_distro == "centos":
                if int(linux_version.split('.')[0]) <= 7:
                    shutil.copy2(os.path.join(package_dir, 'lib', 'libtxl_centos7.so'), '/usr/lib64/libtxl.so')
                else:
                    shutil.copy2(os.path.join(package_dir, 'lib', 'libtxl_centos8.so'), '/usr/lib64/libtxl.so')

            # 复制LYG_TX-server及其他需要的文件
            shutil.copy2(os.path.join(package_dir, 'bin', 'LYG_TX-server'), '/usr/bin/')
            shutil.copy2(os.path.join(package_dir, 'bin', 'libtxl.so'), '/usr/share/')
            shutil.copy2(os.path.join(package_dir, 'bin', 'libgmx.so'), '/usr/share/')
            shutil.copy2(os.path.join(package_dir, 'lib', 'txl.h'), '/usr/include/')

setup(
    name="lyg",
    version="3.8.21",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "distro"  # 用于检测Linux发行版
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows"
    ],
    author="LYG.AI",
    author_email="team@lyg.ai",
    url="https://lyg.ai",
    cmdclass={
        'install': CustomInstall
    }
)

