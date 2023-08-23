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
- [Installation](#installation)
- [Installation From Source](#installation-from-source)
- [Usage](#usage)
- [License](#license)
- [Python Version Support](#python-version-support)

## Introduction

Briefly introduce your project here. Explain its purpose and main features.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/jfarl/superparsenmap

## Installation

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/Superparsenmap)

```bash
# PyPI
pip install superparsenmap
```

## Installation From Source
In the `superparsenmap` directory (same one where you found this file after
cloning the git repo), execute:

	python3 -m build
	pip install dist/superparsenmap-1.0.1.tar.gz

## Usage

In the `superparsenmap` directory (same one where you found this file after
cloning the git repo), execute:

	python superparsenmap.py

	or

	python -m superparsenmap

### Usage Examples:

To run the script with default options:
	
	python superparsenmap.py -i hosts.csv

To specify an output file:

	python superparsenmap.py -i hosts.csv -o hosts.xlsx

To overwrite the output file if it already exists:

	python superparsenmap.py -i input_data.csv -o output_result.xlsx --overwrite

To generate a directory of text files grouped by ports:

	python superparsenmap.py -i hosts.csv --generate_txt

To display help for available operations:

	python superparsenmap.py --help

## License

This project is licensed under the GNU General Public License (GNU GPL). See ``license.txt``

## Python Version Support
This project requires Python 3. It does not support Python 2.
