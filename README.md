# TestParsing

## Supported Operating Systems
- **Linux (Bash):**	CentOS, Debian, Ubuntu
- **Windows (PowerShell):**	10, 2012, 2016

## Prerequisites
- Python 3.9+
## Installation
1. Download **testparsing-main.zip** from GitHub
2. Unzip downloaded file
3. pip install -r requirements.txt

## Usage
**Using command-line arguments only:**
```shell
parser_excel.py --input FileName --output OutputForTotal --mode APPEND/OVERWRITE --delcompany CompanyName
```
**Note:**
1. FileName is name of Excel file for parsing. (required argument)
2. OutputForTotal is name of output Excel File with total calculation. (default value is output.xlsx)
3. APPEND/OVERWRITE :
    1. In case **APPEND** data will be added into database. (default value)
    2. In case **OVERWRITE** data will be replaced in database
4. CompanyName is name of company which should be deleted 

### Limitations
1. No installation module (PyPi not used)
2. Just command line interface realized   
3. Totals Qliq and Qoil are calculated by dates only (no by "fact" or "forecast", for example)
4. Models are not used here. Total calculations are realized by pure SQL
5. Logger module was not used