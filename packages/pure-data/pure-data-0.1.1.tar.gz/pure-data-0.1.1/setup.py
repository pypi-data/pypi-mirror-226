import os
import setuptools
from setuptools import setup


cwd = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(cwd, 'requirements.txt')

with open(file, encoding="utf-8") as f:
    dependencies = list(map(lambda x: x.replace("\n", ""), f.readlines()))

with open("README.md", 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pure-data',
    version = '0.1.1',
    author='BOGDAN PECHENKIN',
    author_email='uberkinder@yandex.com',
    description='Pure Data Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/SimulatorML/Pure-Data',
    install_requires=dependencies,
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)