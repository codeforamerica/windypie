'''
Setup and installation for the package.
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="WindyPie",
    version="0.0.4",
    url="https://github.com/codeforamerica/windypie",
    author="Jesse Bounds",
    author_email="jesse@codeforamerica.org",
    description="An easy-to-use wrapper for the Socrata API",
    packages=[
        'windypie', 'socrata_python'
    ],
    install_requires=[
        'httplib2',
        'configparser',
        'ordereddict',
        'poster'
    ],
    license='BSD-style license; see the file LICENSE for details.',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
