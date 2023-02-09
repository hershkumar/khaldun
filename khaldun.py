# khaldun.py
import re
import subprocess
import sys
import tempfile
import os

# declaring the regex matchers for command/flags
khaldun_command_regexp = re.compile(r'<!---\s*khaldun') # matches "<!--- khaldun" or "<!---khaldun" 
khaldun_closing_regexp = re.compile(r'--->')
khaldun_arg_regexp = re.compile(r'(\w+)="([\w|\s]+)"')

# list of enabled languages
khaldun_langs = ["python", "haskell"]


def run(filepath, new_filepath):
	blocks = {}
	code_input = {}
	code_output = {}
	# get all the code blocks that need to be run, and capture the output
	print("Parsing code blocks...")
	blocks = parse_md(blocks, filepath)
	print("Running code...")
	for name in blocks.keys():
		# find the code and run it
		code_input[name] = get_code(filepath, blocks[name]['input_line'])
		code_output[name] = run_code(code_input[name], blocks[name]['language'])
	print("Inserting code...")
	insert_outputs(filepath, new_filepath, blocks, code_output)
	print("Complete!")


def parse_md(blocks, filepath):
	""" A function that reads the provided markdown file and returns a dict that represents the code blocks that khaldun has to run"""
	fo = open(filepath, "r")

	# function that takes a khaldun command and parses it, and updates the dictionary accordingly
	def format_args(argline) -> dict[str,str]:
		# match the argument regexp
		arg_match = khaldun_arg_regexp.finditer(argline.strip())
		matches = []
		for match in arg_match:
			matches.append(match.group())
		# now iterate through the list and convert it to a dictionary
		args = {}
		for element in matches:
			split = element.split("=")
			args[split[0]] = split[1][1:-1]
		return args

	# function that checks whether the arguments provided in a command are valid
	def check_args(line_num, args) -> bool:
		# determine what type of code block it is
		ktype = args.get('type')
		if ktype != None:
			# input code blocks
			if ktype == "input":
				# check if there exists a language argument
				klang = args.get('language')
				if klang == None:
					print(f"Error: khaldun command at line {line_num} has no specified language.")
					return False
				elif klang not in khaldun_langs:
					print(f"Error: khaldun command at line {line_num} has invalid language specified.")
					return False
				else:
					# check if there is a name argument
					kname = args.get('name')
					if kname == None:
						print(f"Error: khaldun command at line {line_num} has no specified name.")
						return False
					# check if there is a command with that name already
					prev = blocks.get(kname)
					if prev != None:
						print(f"Error: khaldun command at line {line_num} uses name that is already in use.")
						return False
			# output flag
			elif ktype == "output":
				# check if there's a name argument
				kname = args.get('name')
				if kname == None:
					print(f"Error: khaldun command at line {line_num} has no specified name.")
					return False
				else:
					# now check if its been used
					prev = blocks.get(kname)
					if prev == None:
						print(f"Error: khaldun command at line {line_num} specified name that is not previously defined.")
						return False

			# invalid type specified
			else:
				print(f"Error: khaldun command at line {line_num} has invalid type.")
				return False
		else:
			print(f"Error: khaldun command at line {line_num} has no specified type.")
			return False
		return True

	# updates the list of code blocks based on the provided khaldun command
	def update_blocks(line_num, command) -> bool:
		# if the command is an input, we add it to the dict of blocks
		if command.get('type') == "input":
			blocks[command.get('name')] = {'input_line' : (line_num + 1), 'output_line' : -1, 'language' : command.get('language')}
			return True
		if command.get('type') == "output":
			blocks[command.get('name')]['output_line'] = line_num
			return True
		return False

	# iterate through the file
	for line_num, line in enumerate(fo, 1):
		# if the line matches a khaldun command:
		opening_matched = khaldun_command_regexp.match(line)
		if opening_matched != None:
			# match the closing of the command
			closing = khaldun_closing_regexp.search(line)
			
			if closing == None:
				print(f"Error: khaldun commands should be placed on 1 line. (line {line_num})")
			else:
				# get the khaldun arguments
				args = format_args(line[opening_matched.span()[1] : closing.span()[0]])
				if check_args(line_num, args):
					update_blocks(line_num, args)

	fo.close()
	return blocks

# obtains the code in a code block that starts at a given line number
def get_code(filename, start_line) -> str:
	code = ""
	fo = open(filename, "r")
	for line_num, line in enumerate(fo, 1):
		# we ignore all previous lines, as well as the header line, with the tickmarks and the language
		if line_num <= start_line:
			continue
		# the end of the code block
		#TODO: fix the case where there is no newline (not sure if thats possible)
		if line[:-1].endswith('```'):
			# get the line without the tickmarks (and the newline character)
			code += line[:-4]
			break
		else:
			code += line

	fo.close()
	return code

# runs the code given in the language provided, and returns the string output
#TODO: make this work for haskell/any other language
def run_code(code, lang):
	if lang == "python":
		s = subprocess.run([sys.executable,"-c" ,code], capture_output=True).stdout.decode('UTF-8')
	elif lang == "haskell":
		tmp = tempfile.NamedTemporaryFile(suffix=".hs", delete=False, mode='w+', encoding='utf-8')
		try:
			# write the code to the file
			tmp.write(code)
			tmp.read()
			res = subprocess.run(['runhaskell', tmp.name], capture_output=True)
			s = res.stdout.decode('UTF-8')
			# e = res.stderr.decode('UTF-8')
			# print(e)
		finally:
			tmp.close()
			os.unlink(tmp.name)
	else:
		s = "Not Implemented Yet."
	return s

# inserts code into a file at the given line number in the format of a markdown code block
def insert_outputs(filepath, new_filepath, blocks, code_outputs):
	# get a dict of all lines that need to be modified and their modifications
	mods = {}
	for name in blocks.keys():
		mods[blocks[name]['output_line']] = code_outputs[name]
	nfo = open(new_filepath, "w")
	fo = open(filepath, "r")
	for line_num, line in enumerate(fo, 1):
		if line_num not in mods.keys():
			nfo.write(line)
		else:
			nfo.write(line + "\n```\n" + mods[line_num] + "\n```\n")
	nfo.close()
	fo.close()


#TODO: maybe refactor argument system via argparse
#TODO: double check that these arguments are valid
# get the commandline arguments
cl_args = sys.argv[1:]

run(cl_args[0], cl_args[1])

