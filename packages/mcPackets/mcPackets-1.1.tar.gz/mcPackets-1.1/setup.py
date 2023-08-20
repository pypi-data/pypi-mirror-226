from setuptools import setup, find_packages


setup(
    name='mcPackets',
    version='1.1',
    author='朝歌夜弦',
    author_email='top@cvbop.cn',
    description='关于我的世界数据包生存的库!',
    packages=find_packages(),
    install_requires=[
        "nbtlib"
    ],
)

