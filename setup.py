from distutils.core import setup

name = 'troia-python-client'
version = '0.1'


setup(
      name=name,
      version=version,
      description='Troia Python client - uses REST',
      install_requires = [
          'requests',
          'progressbar'
      ],
      packages=["troia_client"],
      )
