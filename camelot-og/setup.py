from setuptools import setup, find_packages
import sys
# from camelot-og.utils.vapi_ei_utils import VAPIEIUtils

if sys.version_info < (2, 7):
    sys.exit('Camelot-pi requires at least Python 2.7, please upgrade and try '
             'again.')

# version = get_tng_version()

dist_requires = []

if 'darwin' in sys.platform:
    dist_requires.append('netifaces')

install_requires = [
    'nose',
    'Fabric==1.14.0',
    'invoke',
    'pycrypto',
    'unittest2',
    'pyparsing',
    'mock',
    'coverage',
    'carnifex',
    'coverage',
    'pep8',
    'enum34',
    'blessings',
    'future']

install_requires.extend(dist_requires)

setup(
    name='Camelot-pi',
    version='12.6.23.0.0.0',
    description='Camelot',
    long_description='',
    # Get strings for classifiers from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers:
    classifiers=[],
    keywords='',
    author='Sateesh Maturi',
    author_email='camelot-og-support@cisco.com',
    url='',
    license='',
    packages=find_packages(
        exclude=['ez_setup', 'examples', 'test', 'contrib', 'doc',
                 'regression']),
    zip_safe=False,
    install_requires=install_requires)
