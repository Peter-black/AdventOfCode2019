def load_program(filename):
	opcode_array = []
	with open(filename) as opcode_file:
		opcode_array = opcode_file.read().split(",")
		opcode_array = [int(i) for i in opcode_array]
	print("[INFO] Successfully loaded program [ "+filename+" ]")
	return opcode_array

def opcode_1(input1, input2):
	return int(input1) + int(input2)

def opcode_2(input1, input2):
	return int(input1) * int(input2)

def opcode_3():
	return input("[INPUT] Enter a value: ")

def opcode_4(input1):
	print("[OUT]: "+str(input1))

def opcode_5(input1):
	return (int(input1) > 0)

def opcode_6(input1):
	return (int(input1) == 0)

def opcode_7(input1, input2):
	return int(int(input1) < int(input2))

def opcode_8(input1, input2):
	return int(int(input1) == int(input2))

def opcode_99():
	pass

def run_opcode_program(opcode_array):
	OP_PARAM_COUNT = { 	1 	: 3,
						2 	: 3,
						3 	: 1,
						4 	: 1,
						5 	: 2,
						6 	: 2,
						7	: 3,
						8	: 3,
						99 	: 0	}

	opcode_pointer = 0
	while True:
		current_instruction = opcode_array[opcode_pointer]

		step_distance = 0
		param_mode = [0,0,0]
		params = [0,0,0]

		#Decode parameter instruction
		val_list = list(str(current_instruction))
		instruction_length = len(val_list)

		#Does it specify an immediate mode?
		if instruction_length > 2:
			current_instruction = (int(val_list[instruction_length - 2]) * 10) + int(val_list[instruction_length - 1])

			#Set the mode per param
			for i in range(OP_PARAM_COUNT[current_instruction]):
				if i + 3 <= instruction_length:
					param_mode[i] = int(val_list[(instruction_length - 3) - i])

		#Apply correct step distance
		step_distance = 1 + OP_PARAM_COUNT[current_instruction]

		#Store param values according to mode
		for i in range(0, OP_PARAM_COUNT[current_instruction]):
			pointer_offset = i + 1

			if param_mode[i] == 1:
				params[i] = opcode_pointer + pointer_offset
			else:
				params[i] = opcode_array[opcode_pointer + pointer_offset]

		#Handle which op it is
		if current_instruction in OP_PARAM_COUNT:
			if current_instruction == 1:
				opcode_array[ params[2] ] = opcode_1( opcode_array[ params[0] ], opcode_array[ params[1] ] )

			elif current_instruction == 2:
				opcode_array[ params[2] ] = opcode_2( opcode_array [params[0] ], opcode_array[ params[1] ] )

			elif current_instruction == 3:
				opcode_array[ params[0] ] = opcode_3()

			elif current_instruction == 4:
				opcode_4( opcode_array[ params[0] ] )

			elif current_instruction == 5:
				if opcode_5( opcode_array[ params[0] ] ):
					opcode_pointer = opcode_array[ params[1] ]
					continue

			elif current_instruction == 6:
				if opcode_6( opcode_array[ params[0] ] ):
					opcode_pointer = opcode_array[ params[1] ]
					continue

			elif current_instruction == 7:
				opcode_array[ params[2] ] = opcode_7( opcode_array[ params[0] ], opcode_array[ params[1] ] )

			elif current_instruction == 8:
				opcode_array[ params[2] ] = opcode_8( opcode_array[ params[0] ], opcode_array[ params[1] ] )

			elif current_instruction == 99:
				opcode_99()
				return 0

		else:
			print("Invalid instruction: " + str(current_instruction))
			break
	
		opcode_pointer = opcode_pointer + step_distance

	return 1 #invalid exit

####################################################################################

program_data = load_program("input.txt")

run_opcode_program(program_data)