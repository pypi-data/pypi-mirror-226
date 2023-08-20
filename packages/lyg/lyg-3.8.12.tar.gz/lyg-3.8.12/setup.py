from setuptools import setup, find_packages
import distro

def get_data_files():
    distro_id = distro.id()
    distro_version = distro.version()

    files = [
        ('/usr/bin', ['bin/LYG_TX-server']),
        ('/usr/share', ['bin/libtxl.so', 'bin/libgmx.so']),
        ('/usr/include', ['lib/txl.h'])
    ]

    if distro_id == "centos":
        if distro_version.startswith('7'):
            files.append(('/usr/lib64', ['lib/libtxl_centos7.so']))
        elif distro_version.startswith('8') or distro_version.startswith('9'):
            files.append(('/usr/lib64', ['lib/libtxl_centos8.so']))

    return files

setup(
    name='lyg',
    version='3.8.12',
    packages=find_packages(),
    package_data={
        'lyg': [
            '*.so',
            '*.pyd'
        ]
    },
    data_files=get_data_files(),
    install_requires=[
        'distro'
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
)

