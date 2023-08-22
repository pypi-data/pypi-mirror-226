# SuperParseNmap: Yet Another (super!) Nmap Parser

|   |  |
| ------------- | ------------- |
| Package  | [![PyPI Latest Release](https://img.shields.io/pypi/v/superparsenmap.svg)](https://pypi.org/project/superparsenmap/) [![PyPI Downloads](https://img.shields.io/pypi/dm/superparsenmap.svg?label=PyPI%20downloads)](https://pypi.org/project/superparsenmap/)  |

SuperParseNmap is a command line utility that parses nmap XML into CSV or Excel format.
It also supports outputting IP address lists to flat files grouped by port for list importing into security tools.

## Table of Contents

- [Introduction](#introduction)
- [Where to Get It](#where-to-get-it)
- [Installation](#installation)
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