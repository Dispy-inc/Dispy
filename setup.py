from setuptools import setup, find_packages

setup(
    name='dispy',
    version='0.0.1',
    description='A python-coded discord bot library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='James French',
    author_email='jamesfrench.contact@gmail.com',
    url='https://github.com/JamesMinoucha/Dispy',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.9.5',
        'websocket_client==1.8.0',
    ],
   classifiers=[
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.12',
      'License :: Creative Commons Attribution 4.0 International',
      'Operating System :: OS Independent',
   ],
   python_requires='>=3.12',
)
