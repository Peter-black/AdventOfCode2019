def load_program(filename):
	opcode_array = []
	with open(filename) as opcode_file:
		opcode_array = opcode_file.read().split(",")
		opcode_array = [int(i) for i in opcode_array]
	print("[INFO] Successfully loaded program [ "+filename+" ]")
	return opcode_array


class Computer:
	def __init__(self):
		self.OP_LIST = { 	1 	: (self._opcode_1 , 3),
							2 	: (self._opcode_2 , 3),
							3 	: (self._opcode_3 , 1),
							4 	: (self._opcode_4 , 1),
							5 	: (self._opcode_5 , 2),
							6 	: (self._opcode_6 , 2),
							7	: (self._opcode_7 , 3),
							8	: (self._opcode_8 , 3),
							99 	: (self._opcode_99 , 0)	}

		self.output_buffer = []
		self.input_buffer = []

		self.opcode_pointer = 0
		self.do_jump = False

		self.user_input = False
		self.awaiting_input = False
		#Used to end the program by opcode 99
		self.terminate = False

	def set_user_input_mode(self, use_user_input):
		self.user_input = use_user_input

	def input(self, input_value):
		self.input_buffer.append(input_value)
		self.awaiting_input = False

	def load_opcode_program(self, program_data):
		self.__init__()
		self.program = list(program_data)

	def run_opcode_program(self):
		
		while not self.terminate and not self.awaiting_input:
			self._update()

		output_return = self.output_buffer
		self.output_buffer = []
		return output_return

	###########################################

	#Location equals sum of inputs
	def _opcode_1(self):
		self.program[ self.params[2] ] = self.program[ self.params[0] ] + self.program[ self.params[1] ] 
	
	#Location equals multiplication of inputs
	def _opcode_2(self):
		self.program[ self.params[2] ] = self.program[ self.params[0] ] * self.program[ self.params[1] ] 
	
	#Location equals a program input
	def _opcode_3(self):
		input_val = None

		if self.user_input:
			input_val = input("[INPUT] Enter a value: ")
		else:
			if len(self.input_buffer) > 0:
				input_val = self.input_buffer.pop(0)
			else:
				self.awaiting_input = True

		self.program[ self.params[0] ] = input_val
	
	#Output a location
	def _opcode_4(self):
		output_val = self.program[ self.params[0] ]
		#print("[OUT]: " + str( output_val ))
		self.output_buffer.append(output_val)
		
	#If location is more than 0, jump to location
	def _opcode_5(self):
		if self.program[ self.params[0] ] > 0:
			self.opcode_pointer = self.program[ self.params[1] ]
			self.do_jump = True
	
	#If location equals 0, jump to location
	def _opcode_6(self):
		if self.program[ self.params[0] ] == 0:
			self.opcode_pointer = self.program[ self.params[1] ]
			self.do_jump = True

	#If input is less than input, set location to 1 or 0
	def _opcode_7(self):
		self.program[ self.params[2] ] = self.program[ self.params[0] ] < self.program[ self.params[1] ]
	
	#If input is equal to input, set location to 1 or 0
	def _opcode_8(self):
		self.program[ self.params[2] ] = self.program[ self.params[0] ] == self.program[ self.params[1] ]
	
	#Terminate
	def _opcode_99(self):
		self.terminate = True

	##############################################

	#Decodes the current instruction and returns the step distance
	def _decode_current_instruction(self):
		self.current_instruction = self.program[self.opcode_pointer]
		self.param_mode = [0,0,0]

		#Decode parameter instruction
		val_list = list(str(self.current_instruction))
		instruction_length = len(val_list)

		#Does it specify an immediate mode?
		if instruction_length > 2:
			self.current_instruction = (int(val_list[instruction_length - 2]) * 10) + int(val_list[instruction_length - 1])

			#Set the mode per param
			for i in range(self.OP_LIST[self.current_instruction][1]):
				if i + 3 <= instruction_length:
					self.param_mode[i] = int(val_list[(instruction_length - 3) - i])

		new_step_distance = 1 + self.OP_LIST[self.current_instruction][1]
		return new_step_distance

	def _apply_params(self):
		self.params = [0,0,0]
		
		#Store param values according to mode
		for i in range(0, self.OP_LIST[self.current_instruction][1]):
			pointer_offset = i + 1

			if self.param_mode[i] == 1:
				self.params[i] = self.opcode_pointer + pointer_offset
			else:
				self.params[i] = self.program[self.opcode_pointer + pointer_offset]

	def _update(self):

		if self.awaiting_input:
			if len(self.input_buffer) == 0:
				return

		step_distance = self._decode_current_instruction()

		self._apply_params()

		#Handle which op it is
		if self.current_instruction in self.OP_LIST:
			self.OP_LIST[self.current_instruction][0]() #calls the op
		else:
			print("Invalid instruction: " + str(self.current_instruction))
			return

		#Don't carry on if we are awaiting input.
		if self.awaiting_input == True:
			return

		#Skip manual pointer updating if we did a jump
		if self.do_jump == True:
			self.do_jump = False
			return

		self.opcode_pointer = self.opcode_pointer + step_distance

####################################################################################

program_data = load_program("input.txt")


highest_output = 0
highest_amp_setup = None

import itertools
possible_amps = list(itertools.permutations([0,1,2,3,4]))

for amp_setup in possible_amps:
	output = [0]
	for i in range(5):
		computer = Computer()
		computer.load_opcode_program(program_data)

		for i in [amp_setup[i], output[0]]:
			computer.input(i)

		output = computer.run_opcode_program()
	
	if output[0] > highest_output:
		highest_output = output[0]
		highest_amp_setup = amp_setup

print("Highest Thruster Output (Single Pass): " +str(highest_output))
print("Best Phase Setup (Single Pass): " +str(highest_amp_setup))

import itertools
possible_amps = list(itertools.permutations([5,6,7,8,9]))

for amp_setup in possible_amps:
	output = [0]
	
	##Set up computers
	computers = []
	for i in range(5):
		computers.append(Computer())
		computers[i].load_opcode_program(program_data)
		computers[i].input(amp_setup[i])#prime the phase setting
	
	terminated = False
	while terminated == False:
		for i in range(5):
			for input_config in [output[0]]:
				computers[i].input(input_config)
				
			output = computers[i].run_opcode_program()
			terminated = computers[i].terminate
		if output[0] > highest_output:
			highest_output = output[0]
			highest_amp_setup = amp_setup

print("Highest Thruster Output (Feedback): " +str(highest_output))
print("Best Phase Setup (Feedback): " +str(highest_amp_setup))