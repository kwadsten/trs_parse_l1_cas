#!/usr/bin/env python3

# ================================================================================
# TRS-80 Parse Level 1 BASIC Cassette File
#
# trs_parse_l1_cas.py
#
# by Kyle Wadsten
# Version 1.0, 08/19/2019
# www.github.com/kwadsten
# ================================================================================

__version__ = '1.0'

import argparse
import sys
import os
from pathlib import Path

# File format (a .cas file can contain multiple programs):
# 	xx bytes = Nulls (0x00)
# 	1 byte   = File Id (0xA5)
# 	2 bytes  = Program starting address HHLL
# 	2 bytes  = Program ending address   HHLL
# 	xx bytes = BASIC program lines      LLHH xxxxxx 0x0D
# 	1 byte   = Checksum

PROGRAM_INFO = f"""TRS-80 Parse Level 1 BASIC Cassette File
by Kyle Wadsten
Version {__version__}, 08/19/2019
www.github.com/kwadsten"""

filedata = None		# Input file as byte array
filedata_idx = 0	# File byte array index
program_number = 0	# A .cas file can contain multiple programs

# -----------------------------
# read_basic_line
# -----------------------------
# Extract a single BASIC line from the bytes array.
# Returns the line as a string (without the ending 0x0D).
#
def read_basic_line():
	global filedata_idx 
	
	line = ''
	
	while True:
		byte = filedata[filedata_idx]
		filedata_idx += 1
		if byte != 0x0D:
			line += chr(byte)
		else:
			break
	return line

# -----------------------------
# main
# -----------------------------
def main():

	global filedata
	global filedata_idx
	
	# Verify python version	
	if sys.version_info < (3,6):
		print(f'Error: This script requires Python 3.6 or higher.')
		exit(1)	
	
	# Get arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('filename', help='input filename (.cas)')
	args = parser.parse_args()
	
	# Verify input file exists
	cas_file = Path(os.path.expanduser(args.filename))
	if not cas_file.is_file():
		print(f'Input file not found: {cas_file}')
		exit(1)
	
	# Read entire file as byte array
	with open(cas_file, 'rb') as f:
		# Read the whole file at once
		filedata = f.read()

	print('=' * 80)
	print(PROGRAM_INFO)	
	print()
	print(f'Input file: {cas_file}')
	print(f'File size: {len(filedata):>6,} (0x{len(filedata):04X})')
	
	while filedata_idx < len(filedata):
		process_program()
		
	print('=' * 80)

# -----------------------------
# process_program
# -----------------------------
# Process a single BASIC program from the bytes array.
# Outputs program metadata and BASIC statements.
#		
def process_program():
		
	global filedata_idx
	global program_number
	
	basic_lines = []
	program_number += 1
	
	# Skip over any non-null header bytes
	pre_null_cnt = 0
	while filedata[filedata_idx] != 0x00:
		filedata_idx += 1
		pre_null_cnt += 1
	
	# Get null header bytes
	null_cnt = 0
	while filedata[filedata_idx] == 0x00:
		filedata_idx += 1
		null_cnt += 1

	# Get file id
	file_id = filedata[filedata_idx]
	filedata_idx += 1

	# Get start address (HHLL)
	start_addr = (filedata[filedata_idx] * 256) + filedata[filedata_idx+1]
	filedata_idx += 2
	
	# Get end address (HHLL)
	end_addr = (filedata[filedata_idx] * 256) + filedata[filedata_idx+1]
	filedata_idx += 2
	
	curr_prog_size = end_addr - start_addr
	first_basic_char = filedata[filedata_idx + 2] # The first BASIC line character after the line number
	
	# Sanity check
	if curr_prog_size < 0 \
	or start_addr == 0xD3D3 \
	or (first_basic_char not in range(ord('A'), ord('Z')) and first_basic_char != ord(' ')):
		print(f'Input file does not appear to be a Level 1 BASIC cassette.')
		exit(1)
	
	# Get BASIC program lines for the current program
	# Format is: LLHH (line number in hex), xxxx (BASIC text), 0D (end of line)
	end_filedata_idx = filedata_idx + curr_prog_size - 1
	while filedata_idx < end_filedata_idx:
		line_number = filedata[filedata_idx] + (filedata[filedata_idx+1] * 256)	# LLHH
		filedata_idx += 2
		line_data = read_basic_line()
		basic_lines.append(str(line_number) + ' ' + line_data)
		
	# Get checksum
	checksum = filedata[filedata_idx]
	filedata_idx += 1

	# Output program metadata and BASIC statements
	print()
	print('-' * 80)
	print(f'Program #{program_number}');
	print('-' * 80)
	print(f'{"Pre-null Count:":>20} {pre_null_cnt:>6}   (0x{pre_null_cnt:02X})');
	print(f'{"Null Count:":>20} {null_cnt:>6}   (0x{null_cnt:02X})');
	print(f'{"File Type:":>20} {file_id:>6}   (0x{file_id:02X})')
	print(f'{"Program Start Addr:":>20} {start_addr:>6,} (0x{start_addr:4X})')
	print(f'{"Program End Addr:":>20} {end_addr:>6,} (0x{end_addr:04X})')
	print(f'{"Program Length:":>20} {end_addr - start_addr + 1:>6,} (0x{end_addr - start_addr + 1:04X})')
	print(f'{"Checksum:":>20} {file_id:>6}   (0x{checksum:02X})')
	print('-' * 80)

	# Output BASIC program
	print('\n'.join(basic_lines))

# -----------------------------
# Program Entry Point
# -----------------------------
if __name__== "__main__":
	main()