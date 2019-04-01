import sys

from setuptools import setup, find_packages


def forbid_publish():
    argv = sys.argv
    blacklist = ['register', 'upload']

    for command in blacklist:
        if command in argv:
            values = {'command': command}
            print('Command "%(command)s is not allowed... ' % values)
            sys.exit(2)


forbid_publish()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gmail-sender',
      version='1.0.0',
      description='Python module for sending messages with Gmail',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alec Wiseman',
      author_email='alec.wiseman@gmail.com',
      packages=find_packages(),
      install_requires=['google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib'],
      extras_require={
          'dev': ['check-manifest'],
          'test': ['coverage']
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Tools',
          'Programming Language :: Python :: 3.7'
      ],
      entry_points={
          'console_scripts': [
              'gmail-sender=gmail_sender.__main__:main'
          ]
      })
