import sys
import setuptools


requirements = []

if sys.version_info < (2, 6):
    requirements.append('simplejson')
if sys.version_info < (2, 7):
    requirements.append('argparse')

setuptools.setup(
    name="faucet",
    version="0.1",
    description="OpenStack Load Balancer Server",
    long_description="OpenStack Load Balancer Server",
    url='https://github.com/ljjjustin/faucet',
    license='Apache',
    author='Jiajun Liu',
    author_email='iamljj@gmail.com',
    packages=setuptools.find_packages(exclude=['bin', 'tests', 'tools']),
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=requirements,
    scripts=[
        'bin/faucet-server',
    ],
)
