from setuptools import find_packages, setup

setup(
  name = 'motty',
  packages = ['motty'],
  version = '1.0',
  description = 'utils for http mocking',
  author = 'David Lee',
  author_email = 'scalalang2@gmail.com',
  include_package_data = True,
  scripts=['motty/runmotty.py'],
  entry_points={'console_scripts': [
    'run-motty = runmotty:run_motty',
  ]},
  install_requires=['django', 'djangorestframework', 'django-libsass', 'libsass', 'django-compressor',
    'django-sass-processor', 'tornado'],
  url = 'https://github.com/scalalang2/motty', # use the URL to the github repo
  keywords = ['mocking', 'motty', 'http'], # arbitrary keywords
  classifiers=[ 
  ],
)
