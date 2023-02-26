# MEGAsync Parser

A python-based tool to extract data from MEGAsync Windows application database file and generate a CSV with all the files that are present on MEGA cloud.

Location of database file on Windows systems: `"%LocalAppData%\Mega Limited\MEGAsync\megaclient_statecache13_<RANDOM 36 chars>.db"`

## Requirements

Python 3.9 or above. The older versions of Python 3.x should work fine as well.

## Dependencies

These are the required libraries needed to run this script.

+ argparse
+ csv
+ os
+ sqlite3

## Usage

This is a CLI based tool.

```bash
python3 MEGAsyncParser.py -f <path to megaclient_statecache13_<RANDOM 36 chars>.db>
```

![](https://i.imgur.com/5kcgoYB.png)

To view the help:

```bash
python3 MEGAsyncParser.py -h
```

![](https://i.imgur.com/XogJ5bF.png)

## Author 👥

B. Krishna Sai Nihith
+ Twitter: [@_Nihith](https://twitter.com/_Nihith)
+ Personal Blog: https://g4rud4.gitlab.io