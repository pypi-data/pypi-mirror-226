
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="aioTrends",
    packages=["aioTrends"],
    version="0.0.4",
    license="MIT",
    description="Library for fetching Google Trends in an async. way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stephen Zhang",
    author_email="stephen_se@outlook.com",
    url="https://github.com/yuz0101/aioTrends",
    download_url='https://github.com/yuz0101/aioTrends/archive/refs/tags/v_04.tar.gz',
    keywords=['google', 'trends', 'async', 'asyncio', 'aiohttp', 'googletrends', 'pytrends'],
    install_requires=["numpy", "pandas", "requests", "aiohttp", "aiofiles", "colorama", "matplotlib"],
    
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],

)