from setuptools import find_packages
from setuptools import setup

setup(name = 'key_recorder_and_player',
      description = 'Package for recording and replaying keystrokes.',
      author = 'T. Rose',
      url = 'https://github.com/timcrose/key_recorder_and_player',
      packages = find_packages(),
      install_requires = ['pynput', 'pandas']
     )
