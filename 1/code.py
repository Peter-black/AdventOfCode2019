import math

def calc_fuel(mass):
	fuel = (math.floor(mass / 3) - 2)
	if fuel < 0:
		fuel = 0
	return fuel


fuel_sum = 0

with open("input.txt") as module_input:
	for line in module_input.read().split("\n"):
		module_size = int(line) 
		amount_of_fuel = calc_fuel(module_size)

		while True:
			if amount_of_fuel == 0:
				break

			fuel_sum = fuel_sum + amount_of_fuel
			amount_of_fuel = calc_fuel(amount_of_fuel)

print("--------------------------")
print("fuel_sum")
print(fuel_sum)