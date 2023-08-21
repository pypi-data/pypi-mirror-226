from setuptools import setup, find_packages

setup(
    name='variablz_qt',
    version='0.0.2',
    description='''Welcome to the Variablz QT Library! This library provides a collection of utility functions tailored 
    for software developers using PyQt libraries It's designed to 
    simplify common tasks, enhance productivity, and facilitate learning, especially for students at Variablz 
    Academy.''',
    packages=find_packages(),
    install_requires=['certifi==2023.7.22',
                      'charset-normalizer==3.2.0',
                      'docopt==0.6.2',
                      'idna==3.4',
                      'pipreqs==0.4.13',
                      'PyQt6==6.5.2',
                      'PyQt6-Qt6==6.5.2',
                      'PyQt6-sip==13.5.2',
                      'requests==2.31.0',
                      'urllib3==2.0.4',
                      'yarg==0.1.9',
                      ],
)
