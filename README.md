# TestParsing

## Supported Operating Systems
- **Linux (Bash):**	CentOS, Debian, Ubuntu
- **Windows (PowerShell):**	10, 2012, 2016

## Prerequisites
- Python 3.9+
```shell
pip install -r requirements.txt
```
## Installation
1. Download **testparsing.zip** from GitHub
2. Unzip 

## Usage
**Using command-line arguments only:**
```shell
parser_excel.py --input FileName --output OutputForTotal --mode APPEND/OVERWRITE --delcompany CompanyName
```
**Note:**
1. FileName is name of Excel file for parsing.
2. OutputForTotal is name of output Excel File with total calculation
3. APPEND/OVERWRITE :
    1. In case **APPEND** data will be added into database 
    2. In case **OVERWRITE** data will be replaced in database
4. CompanyName is name of company which should be deleted 
