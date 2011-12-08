from distutils.core import setup

name = 'dsas-client'
version = '0.1'


setup(
      name=name,
      version=version,
      description='Python DSaS client - using REST',
      #py_modules=['dsas.rest_dsas_client'],
      packages=["dsas"],
      )
