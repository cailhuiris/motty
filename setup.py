from setuptools import find_packages, setup

setup(
  name = 'motty',
  packages = ['motty'], # this must be the same as the name above
  version = '0.1',
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
  download_url = 'https://github.com/scalalang2/motty/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['mocking', 'motty', 'http'], # arbitrary keywords
  classifiers=[ 
  ],
)
