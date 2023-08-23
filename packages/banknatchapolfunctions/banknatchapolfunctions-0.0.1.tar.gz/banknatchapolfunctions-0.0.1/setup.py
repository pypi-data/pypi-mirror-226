from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='banknatchapolfunctions',
  version='0.0.1',
  description='ฟังก์ชันของ Bank Natchapol',
  long_description=open('README.txt', encoding='utf8').read() + '\n\n' + open('CHANGELOG.txt', encoding='utf8').read(),
  url='',  
  author='Bank Natchapol',
  author_email='natchapol.pat@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='banknatchapol', 
  packages=find_packages(),
  install_requires=['numpy', 'pandas', 'matplotlib'] 
)