import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content

README = read_file('README.rst')
CHANGELOG = read_file('CHANGELOG.rst')
CONTRIBUTORS = read_file('CONTRIBUTORS.rst')

REQUIREMENTS = [
    "kinto-http",
]

ENTRY_POINTS = {
    'console_scripts': [
        'kinto-wizard = kinto.__main__:main'
    ]
}


setup(name='kinto-wizard',
      version='0.1.0.dev0',
      description='kinto-wizard is a tool to configure a kinto server from an YAML file.',
      long_description=README + "\n\n" + CHANGELOG + "\n\n" + CONTRIBUTORS,
      license='Apache License (2.0)',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Internet :: WWW/HTTP",
          "License :: OSI Approved :: Apache Software License"
      ],
      keywords="web sync json storage services",
      author='Mozilla Services',
      author_email='storage-team@mozilla.com',
      url='https://github.com/Kinto/kinto-wizard',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=REQUIREMENTS,
      test_suite="tests",
      entry_points=ENTRY_POINTS)