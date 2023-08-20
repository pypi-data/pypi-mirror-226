from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Algida ile kazan unofficial api'


# Setting up
setup(
    name="Alika",
    version=VERSION,
    author="WarF0rPeace",
    description=DESCRIPTION,
    packages=find_packages() + ['alika/api'],
    install_requires=['requests'],
    keywords=['python', 'unofficial api'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)