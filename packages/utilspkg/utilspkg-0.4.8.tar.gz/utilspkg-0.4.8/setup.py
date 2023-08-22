import os
# from setuptools import setup
from setuptools import setup, find_packages

os.chdir('/Users/croft/VScode/ptacorechallenge/utilsfolder')

setup(
    name='utilspkg',
    version='0.4.8',
    packages=find_packages(include=['utilspkg']),
    install_requires=[
        'airtable-python-wrapper>=0.15.3',
        'openai>=0.27.7',
        'protobuf>=4.24.1',
        'python-dotenv>=1.0.0',
        'pytz>=2023.3',
        'slack-sdk>=3.21.3',
        'tenacity>=8.2.2',
        'PyYAML',
        'google-cloud-logging'
    ]
)
