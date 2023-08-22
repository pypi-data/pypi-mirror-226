import sys
import time
from setuptools import find_packages, setup

install_requires = ['cryptography', 'notebuild']

setup(name='farfuntool',
      version=time.strftime("%Y%m%d%H%M", time.localtime()),
      description='funtool',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',

      packages=find_packages(),
      install_requires=install_requires
      )
