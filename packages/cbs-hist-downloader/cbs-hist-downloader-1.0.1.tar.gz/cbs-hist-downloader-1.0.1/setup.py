from setuptools import setup, find_packages

setup(
    name='cbs-hist-downloader',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver_manager'
    ],
)

