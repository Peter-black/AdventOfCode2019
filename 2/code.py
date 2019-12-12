def load_program(filename):
	opcode_array = []
	with open(filename) as opcode_file:
		opcode_array = opcode_file.read().split(",")
		opcode_array = [int(i) for i in opcode_array]
	return opcode_array

def opcode_1(input_pos1, input_pos2):
	return input_pos1 + input_pos2

def opcode_2(input_pos1, input_pos2):
	return input_pos1 * input_pos2

def opcode_99():
	pass

def run_opcode_program(opcode_array):
	STEP_DISTANCE = 4
	VALID_CODES = [1, 2, 99]

	opcode_pointer = 0
	while True:
		current_instruction = opcode_array[opcode_pointer]
	
		if current_instruction in VALID_CODES:
			if current_instruction == 1:
				opcode_array[opcode_array[opcode_pointer+3]] = opcode_1( opcode_array[opcode_array[opcode_pointer+1]], opcode_array[opcode_array[opcode_pointer+2]] )
			elif current_instruction == 2:
				opcode_array[opcode_array[opcode_pointer+3]] = opcode_2( opcode_array[opcode_array[opcode_pointer+1]], opcode_array[opcode_array[opcode_pointer+2]] )
			elif current_instruction == 99:
				opcode_99()
				break
		else:
			print("Invalid instruction: " + str(current_instruction))
			break
	
		opcode_pointer = opcode_pointer + STEP_DISTANCE

	return opcode_array[0]

####################################################################################

program_data = load_program("input.txt")

#RESTORE STATE TO 1202
onetwozerotwo_program = list(program_data)
onetwozerotwo_program[1] = 12
onetwozerotwo_program[2] = 2
onetwozerotwo_output = run_opcode_program(onetwozerotwo_program)
print("1202 Output: " + str(onetwozerotwo_output) )

#Brute force the input for 19690720
found_value = False

for noun in range(0, 100):
	if found_value:
		break

	for verb in range (0, 100):
		if found_value:
			break

		bruteforce_program = list(program_data)
		bruteforce_program[1] = noun
		bruteforce_program[2] = verb
		if run_opcode_program(bruteforce_program) == 19690720:
			print("Found inputs: noun = "+str(noun)+" verb = "+str(verb))
			found_value = True
