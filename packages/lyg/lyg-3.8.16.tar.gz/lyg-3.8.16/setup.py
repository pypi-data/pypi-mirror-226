from setuptools import setup, find_packages, Command
from setuptools.command.install import install
import os
import shutil
import distro

class CustomInstall(install):
    def run(self):
        install.run(self)
        
        if os.name == "posix":
            if os.getuid() != 0:
                raise PermissionError("You must run this with root privileges to install files in system directories.")
            
            # Post-install script for Linux
            linux_distro = distro.id()
            linux_version = distro.version()

            if linux_distro == "centos":
                if int(linux_version.split('.')[0]) <= 7 and os.path.exists('lyg/lib/libtxl_centos7.so'):
                    shutil.copy2('lyg/lib/libtxl_centos7.so', '/usr/lib64/libtxl.so')
                else:
                    shutil.copy2('lyg/lib/libtxl_centos8.so', '/usr/lib64/libtxl.so')

            shutil.copy2('lyg/bin/LYG_TX-server', '/usr/bin/')
            shutil.copy2('lyg/bin/libtxl.so', '/usr/share/')
            shutil.copy2('lyg/bin/libgmx.so', '/usr/share/')
            shutil.copy2('lyg/lib/txl.h', '/usr/include/')

setup(
    name="lyg",
    version="3.8.16",
    packages=find_packages(),
    package_data={
        'lyg': ['*.so', '*.pyd', 'bin/*', 'lib/*']
    },
    include_package_data=True,
    install_requires=[
        "distro"  # 用于检测Linux发行版
    ],
    cmdclass={'install': CustomInstall},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows"
    ],
    author="LYG.AI",
    author_email="team@lyg.ai",
    url="https://lyg.ai"
)

