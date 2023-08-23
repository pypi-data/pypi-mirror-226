# SuperParseNmap: Yet Another (super!) Nmap Parser

|   |  |
| ------------- | ------------- |
| Package  | ![PyPI - Status](https://img.shields.io/pypi/status/superparsenmap) [![Upload Python Package](https://github.com/jfarl/superparsenmap/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jfarl/superparsenmap/actions/workflows/python-publish.yml) [![PyPI Latest Release](https://img.shields.io/pypi/v/superparsenmap.svg)](https://pypi.org/project/superparsenmap/) ![PyPI - License](https://img.shields.io/pypi/l/superparsenmap) |

SuperParseNmap is a command line utility that generates files containing open port summaries from nmap XML.
- Supported outputs are CSV and Excel. Excel will contain additional sheets split grouped by port number and containing correlated IP addresses.
- Additional option for outputting IP address lists to flat files grouped by port for importing into command-line interface security tools.

## Table of Contents

- [Introduction](#introduction)
- [Where to Get It](#where-to-get-it)
- [Recommended Installation](#recommended-installation)
- [pip Installation From Source](#pip-installation-from-source)
- [Manual Usage](#manual-usage)
- [License](#license)
- [Python Version Support](#python-version-support)

## Introduction

Briefly introduce your project here. Explain its purpose and main features.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/jfarl/superparsenmap

## Recommended Installation

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/Superparsenmap)

```bash
# PyPI
pip install superparsenmap
```

## pip Installation From Source
In the `superparsenmap` directory (same one where you found this file after
cloning the git repo), execute:

	python3 -m build
	pip install dist/superparsenmap-1.x.x.tar.gz

## Manual Usage

In the `superparsenmap` directory (same one where you found this file after
cloning the git repo), execute:

	# Build the project first
	python3 -m build
 
Then,

	python superparsenmap.py

	or

	python -m superparsenmap

### Usage Examples:

To run the script with minimum required options:
	
	superparsenmap -i nmap_results.xml

To specify an output file:

	superparsenmap -i nmap_results.xml -o hosts --excel

To overwrite the output file if it already exists:

	superparsenmap -i nmap_results.xml -o output_result --overwrite

To generate a directory of text files grouped by ports:

	superparsenmap -i nmap_results.xml --txt

To display help for available operations:

	superparsenmap --help

## License

This project is licensed under the GNU General Public License (GNU GPL). See ``license.txt``

## Python Version Support
This project requires Python 3. It does not support Python 2.
