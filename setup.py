from setuptools import setup, find_packages

setup(
    name='dispy-bot',
    version='0.1.0.6',
    description='A python-coded discord bot library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='James French',
    author_email='jamesfrench.contact@gmail.com',
    url='https://github.com/JamesMinoucha/Dispy',
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.11",
        "setuptools>=75.6.0",
        "websocket_client>=1.8.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)