from setuptools import setup
from pathlib import Path

readme_path = Path.cwd() / "README.md"
long_description = readme_path.read_text()

exec(open('superparsenmap/version.py').read())

setup(
    name='superparsenmap',
    packages=['superparsenmap'],
    version=__version__,
    description='SuperParseNmap is a command line utility that parses nmap XML into CSV or Excel format.',
    long_description=long_description,
    author='Jonathan Farley',
    author_email='jonffarley@gmail.com',
    url='https://github.com/jfarl/superparsenmap',
    keywords = ['nmap', 'parser', 'excel', 'csv'],
    license='GPLv3+',
    install_requires=[
        'pandas==1.5.3',
        'python_libnmap==0.7.3',
    ],
    scripts=[''],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Security',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)