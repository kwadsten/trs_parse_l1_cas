# TRS-80 Parse Level 1 BASIC Cassette File

A Python script to extract Level 1 BASIC programs from a .cas file.

I wrote this script to extract the BASIC programs from some Level 1 CLOAD magazine .cas files in order to convert them to Level 2 BASIC.

I hope it might be useful to other TRS-80 Level 1 users as well.

Please note that a single .cas file can contain multiple BASIC programs.

## Requirements

Python 3.6 or higher

## Usage
    usage: trs_parse_l1_cas.py [-h] [-v] filename

    positional arguments:
      filename       input filename (.cas)

    optional arguments:
      -h, --help     show this help message and exit
  
## Example Output
    ================================================================================
    TRS-80 Parse Level 1 BASIC Cassette File
    by Kyle Wadsten
    Version 1.0, 08/19/2019
    www.github.com/kwadsten

    Input file: /Users/kpw/Desktop/hello.cas
    File size:    172 (0x00AC)

    --------------------------------------------------------------------------------
    Program #1
    --------------------------------------------------------------------------------
         Pre-null Count:      0   (0x00)
             Null Count:    128   (0x80)
              File Type:    165   (0xA5)
     Program Start Addr: 16,896 (0x4200)
       Program End Addr: 16,934 (0x4226)
         Program Length:     39 (0x0027)
               Checksum:    165   (0x56)
    --------------------------------------------------------------------------------
    10  CLS
    20  PRINT "HELLO WORLD!"
    30  END
    ================================================================================

