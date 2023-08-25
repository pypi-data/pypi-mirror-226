from setuptools import setup, find_packages, Extension

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open("README.md", "r",encoding="utf-8") as fh:
    README_description = fh.read()

with open("CHANGELOG.md", "r",encoding="utf-8") as fh:
    CHANGELOG_description = fh.read()

with open("USAGE.md", "r",encoding="utf-8") as fh:
    USAGE_description = fh.read()

setup(
    name='pymeili',
    version='0.2.11',
    description='a module to beautify your python plot or terminal text.',
    long_description=README_description + '\n\n' + USAGE_description + '\n\n' + CHANGELOG_description,
    long_description_content_type='text/markdown',
    url='',
    author='VVVictorZhou',
    author_email='vichouro@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='beautify',
    packages=find_packages(),
    install_requires=['']
)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# 獲取當前檔案位址
currentfilepath = __file__

# 刪去__file__中最後面自"\"開始的字串(刪除檔名)
motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]
print('Current font folder path: '+bcolors.OKBLUE+f'{motherpath}'+bcolors.ENDC)
import os
# go to motherpath
os.chdir(motherpath)
# clone github respository
os.system(f'git clone https://github.com/VVVICTORZHOU/resources.git')
print(f'[HINT] Try to clone github font respository into {motherpath}.')
print(f'[HINT] Make sure the font files are in the directory:\n\t 1. {motherpath}\\futura medium bt.ttf\n\t 2. {motherpath}\\Futura Heavy font.ttf\n\t 3. {motherpath}\\Futura Extra Black font.ttf')
print(f'\033[93m [HINT] If no, please install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder: {motherpath}. \033[0m')