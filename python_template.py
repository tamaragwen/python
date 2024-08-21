#!/Users/gwen/opt/anaconda3/bin/python

# standard libraries
import sys
from datetime import datetime, timedelta
import argparse
import inspect
import logging

DT_FMT = '%Y-%m-%d %H:%M:%S.%f'
PROGRAM_NAME = sys.argv[0]
PROGRAM_DESC = 'This program does ... '
BYLINE = 'Created by Gwen Nicodemus.'
TODAY = datetime.strftime(datetime.now(),DT_FMT)
LOG_NAME = f'{PROGRAM_NAME}_{TODAY.split()[0]}.log'
logging.basicConfig(level = logging.DEBUG,
	format = "%(levelname)s:%(name)s:%(message)s",
	datefmt = "%Y-%m-%d %H:%M",
        filename = LOG_NAME,
        encoding = "utf-8",
        filemode = "a"
)
logging.info(f'New Run')
logging.info(f'Timestamp = {datetime.now()}')

def bad_argument(err, arg, value, module):
	'''Generate end print error message when bad arguments are used.'''
	module = f'{str(module).split()[-1][0:-1]}'
	msg = f'\nAn invalid argument was used.\n\t{arg = }\n\t{value = }\n\t{err = }\n'
	msg = f'{msg} Module: {module}'
	logging.error(msg)
	print (msg)
	print (f'Run {PROGRAM_NAME} -h for help.\n\n')
	exit()

def validate_file_name(file_name:str) -> bool:
	''' Check to see if the file_name is writeable. '''
	logging.info(f'checkinng file name {file_name = }')
	try:
		handler = open(file_name, 'w')
		handler.close()
	except Exception as err:
		bad_argument(err, '--output or -o', file_name, inspect.currentframe())
		exit (1)
	return file_name

def validate_integer(number:str) -> int:
	''' Check to see if string contains a valid integer. Return int. '''
	logging.info(f'Checking number {number = }')
	try:
		num = int(str(number).strip())
	except ValueError as err:
		bad_argument(err, '--num_lines or -n', number, inspect.currentframe())
	return num

def get_args() -> (int, str, bool):
	'''Parse the arguments given to the program.'''
	logging.info('Module: get_args')
	parser = argparse.ArgumentParser(
		prog = PROGRAM_NAME,
		description = PROGRAM_DESC,
		epilog = BYLINE)
	parser.add_argument('-f', '--flag', 
		action = 'store_true', 
		help = 'true/false argument, like -a in ls')
	parser.add_argument('-i', '--int_number',
		default = 1000,
		help = 'what this arg is used for, default = 1000')
	parser.add_argument('-o', '--output',
		default = './banana.log',
		help = 'output file name, default is ./banana.log')
	args = parser.parse_args()
	int_number = validate_integer(args.int_number)
	output_file = validate_file_name(args.output)
	flag = args.flag
	logging.info(f'{int_number = } - {output_file = } - {flag}')
	return int_number, output_file, flag

def write_file(output_file:str, page:list) -> None:
	''' Write page:list out to a flat file, line by line '''
	logging.info(f'Module: write_file, {output_file = }')
	handler = open(output_file, 'w')
	for line in page:
		handler.write(f'{line}')
	handler.close()

def get_times(days_before:int = 7, 
	days_after:int = 7, 
	full_days:bool = True,
	return_strings:bool = True) -> (datetime, datetime, datetime):
	''' Return three dates. Full dates has before start at midnight and
            after stop at 11:59:59; now stays the same
	    return_strings returns string output, else datetime objects. '''
	logging.info(f'Module get_times {days_after = } {days_before = }')
	logging.info(f'{full_days = } {return_strings = }')
	now = datetime.now()
	before = now - timedelta(days = 7)
	after = now + timedelta(days = 7)
	if full_days:
		before = before.replace(hour=0, minute=0, second=0, microsecond=0)
		after = after.replace(hour=11, minute=59, second=59, microsecond=999999)
	if return_strings:
		before = datetime.strftime(before, DT_FMT)
		now = datetime.strftime(now, DT_FMT)
		after = datetime.strftime(after, DT_FMT)
	return before, now, after

int_number, output_file, flag = get_args()
print (f'\n\n{int_number = }')
print (f'{output_file = }')
print (f'{flag  = }')

write_file(output_file, ['example','text'])
print ('\n\n')
before, now, after = get_times()
print (f'{before = }')
print (f'{now = }')
print (f'{after = }\n\n')
logging.info('w00t! finsihed')
logging.info('\n')
