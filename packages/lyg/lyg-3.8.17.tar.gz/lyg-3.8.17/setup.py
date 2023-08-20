import os
import shutil
import distro
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        install.run(self)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        if os.name == "posix":
            if os.getuid() != 0:
                raise PermissionError("You must run this with root privileges to install files in system directories.")

            linux_distro = distro.id()
            linux_version = distro.version()

            if linux_distro == "centos":
                if int(linux_version.split('.')[0]) <= 7:
                    lib_path = os.path.join(script_dir, 'lyg', 'lib', 'libtxl_centos7.so')
                    shutil.copy2(lib_path, '/usr/lib64/libtxl.so')
                else:
                    lib_path = os.path.join(script_dir, 'lyg', 'lib', 'libtxl_centos8.so')
                    shutil.copy2(lib_path, '/usr/lib64/libtxl.so')

            binary_path = os.path.join(script_dir, 'lyg', 'bin', 'LYG_TX-server')
            shutil.copy2(binary_path, '/usr/bin/')

            # Copy other necessary files as per your requirements
            shutil.copy2(os.path.join(script_dir, 'lyg', 'bin', 'libtxl.so'), '/usr/share/')
            shutil.copy2(os.path.join(script_dir, 'lyg', 'bin', 'libgmx.so'), '/usr/share/')
            shutil.copy2(os.path.join(script_dir, 'lyg', 'lib', 'txl.h'), '/usr/include/')

setup(
    name='lyg',
    version='3.8.17',
    packages=find_packages(),
    install_requires=[
        "distro"  # 用于检测Linux发行版
    ],
    include_package_data=True,
    entry_points={
        # Define any entry points if necessary
    },
    cmdclass={
        'install': CustomInstall,
    },
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
)

