with open("input.txt") as wires_input:
	both_wires_paths = wires_input.read().split("\n")
	first_wires_path = both_wires_paths[0].split(",")
	second_wires_path = both_wires_paths[1].split(",")

#Filled with { (x, y) : (id, steps) }
locations_visted = {}

def do_move(coords, direction, total_steps, id, locations_visted):
	if direction == "L":
		coords[0] = coords[0] - 1

	elif direction == "R":
		coords[0] = coords[0] + 1

	elif direction == "D":
		coords[1] = coords[1] + 1

	elif direction == "U":
		coords[1] = coords[1] - 1

	total_steps = total_steps + 1

	#If coord has been registered
	if (coords[0], coords[1]) in locations_visted:

		#if it was us, then ignore it.
		if locations_visted[(coords[0],coords[1])][0] == id:
			 return total_steps

		#If it was them then update it. [conflict id, sum of steps]
		locations_visted[(coords[0], coords[1])] = [3, locations_visted[(coords[0], coords[1])][1] + total_steps]
	else:
		#Regular ol register
		locations_visted[(coords[0], coords[1])] = [id, total_steps]

	return total_steps

def trace_path(path, id, locations_visted):
	wire_location = [0,0]
	step_count = 0
	for i, move in enumerate(path):
		direction = path[i][0]
		distance = int(path[i][1:])

		for j in range(distance):
			step_count = do_move(wire_location, direction, step_count, id, locations_visted)

trace_path(first_wires_path, 1, locations_visted)
trace_path(second_wires_path, 2, locations_visted)

smallest_manhattan = 99999999999999999
for coord in locations_visted:
	if locations_visted[coord][0] == 3:
		manhattan = abs(coord[0]) + abs(coord[1])
		if manhattan < smallest_manhattan:
			smallest_manhattan = manhattan

print("Smallest Manhattan: "+str(smallest_manhattan))

fewest_steps = 999999999999999
for coord in locations_visted:
	if locations_visted[coord][0] == 3 and locations_visted[coord][1] < fewest_steps:
		fewest_steps = locations_visted[coord][1]

print("Fewest Steps: "+str(fewest_steps))