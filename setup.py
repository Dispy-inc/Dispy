from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name='dispy-bot',
    version='0.1.0.7',
    description='A python-coded discord bot library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='James French',
    author_email='jamesfrench.contact@gmail.com',
    url='https://github.com/JamesMinoucha/Dispy',
    packages=find_packages(),
    install_requires=required_packages,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)