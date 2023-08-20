import os
from setuptools import setup, find_packages
import distro
from setuptools.command.install import install

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
                if int(linux_version.split('.')[0]) <= 7 and os.path.exists('lib/libtxl_centos7.so'):
                    os.rename('lib/libtxl_centos7.so', '/usr/lib64/libtxl.so')
                elif os.path.exists('lib/libtxl_centos8.so'):
                    os.rename('lib/libtxl_centos8.so', '/usr/lib64/libtxl.so')

data_files_entries = []
if os.name != "nt":  # Not Windows
    data_files_entries.extend([
        ('/usr/bin', ['bin/LYG_TX-server']),
        ('/usr/share', ['bin/libtxl.so', 'bin/libgmx.so']),
        ('/usr/include', ['lib/txl.h']),
        ('/usr/lib64', ['lib/libtxl_centos7.so', 'lib/libtxl_centos8.so'])
    ])

setup(
    name='lyg',
    version='3.8.13',
    packages=find_packages(),
    install_requires=[
        'distro;platform_system=="Linux"'
    ],
    package_data={
        'lyg': [
            '*.so',
            '*.pyd'
        ]
    },
    data_files=data_files_entries,
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
        'install': CustomInstall,
    }
)

