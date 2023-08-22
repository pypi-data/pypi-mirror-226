from setuptools import setup, find_packages, Extension

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pymeili',
    version='0.2.1',
    description='a module to beautify your python plot.',
    long_description=open('README.md',encoding="utf-8").read() + '\n\n' + open('CHANGELOG.txt',encoding="utf-8").read(),
    url='',
    author='VVVictorZhou',
    author_email='vichouro@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='beautify',
    packages=find_packages(),
    install_requires=['']
)



# 獲取當前檔案位址
currentfilepath = __file__

# 刪去__file__中最後面自"\"開始的字串(刪除檔名)
motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]
print(f'[HINT] Please install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder: {motherpath}.')