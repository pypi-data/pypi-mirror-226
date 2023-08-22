from setuptools import setup, find_packages

setup(
    name='quickdate', 
    version='0.0.2', 
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/cador/quickdate',
    author='Haolin You',
    author_email='cador.ai@aliyun.com', 
    description='快捷处理日期的Python库, 支持从字符串解析日期, 灵活实现加减日、周、月、年、时、分、秒的时间操作', 
    install_requires=[
        'datetime',
        'python-dateutil'
    ],
)
