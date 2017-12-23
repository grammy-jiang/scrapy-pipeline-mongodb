from setuptools import find_packages
from setuptools import setup

import versioneer

extras_require = {}

setup(
    name='scrapy-pipeline-mongodb',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url='https://github.com/grammy-jiang/scrapy-pipeline-mongodb',
    description='',
    long_description=open('README.rst').read(),
    author='Grammy Jiang',
    maintainer='Grammy Jiang',
    maintainer_email='grammy.jiang@gmail.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'txmongo',
        'scrapy>=1.4.0'
    ],
    extras_require=extras_require,
)
