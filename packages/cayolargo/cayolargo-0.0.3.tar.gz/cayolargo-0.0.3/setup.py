import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.3'
PACKAGE_NAME = 'cayolargo'
AUTHOR = 'Pawel Lachowicz'
AUTHOR_EMAIL = 'enquiries@quantatrisk.com'
URL = ''

LICENSE = 'MIT'
DESCRIPTION = 'Python library for Cryptocurrency Markets Analysis and Crypto Algo-Trading'
LONG_DESCRIPTION = LONG_DESCRIPTION = (HERE / "README.md").read_text()

LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'python-binance==1.0.17',
      'matplotlib',
      'requests'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
