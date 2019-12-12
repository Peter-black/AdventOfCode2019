with open("input.txt") as orbitmap_file:
	orbitmap = orbitmap_file.read().split("\n")

direct_orbits = {}

for orbit in orbitmap:
	orbit_components = orbit.split(")")

	if orbit_components[1] in direct_orbits:
		direct_orbits[orbit_components[1]].append(orbit_components[0])
	else:
		direct_orbits[orbit_components[1]] = [ orbit_components[0] ]

def path_to_home(direct_orbits, from_where):
	path = []
	
	while from_where in direct_orbits:
		from_where = direct_orbits[from_where][0]
		path.append(from_where)
		if from_where == 'COM':
			return path

total = 0 
for orbit in direct_orbits:
	total = total + len(path_to_home(direct_orbits, orbit))

print("Total Number of Orbits: "+str(total))

you_path = path_to_home(direct_orbits, 'YOU')
san_path = path_to_home(direct_orbits, 'SAN')

steps_taken = 0
for i, val in enumerate(you_path):
	if val in san_path:
		print("Shortest Path to Santa: "+ str(steps_taken + san_path.index(val)) )

		break
	steps_taken = steps_taken + 1