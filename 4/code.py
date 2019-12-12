LENGTH = 6
MIN = 387638
MAX = 919123

passed_number_count = 0
strict_passed_number_count = 0

for num in range(MIN, MAX):
	num_list = list(str(num))

	dupe_check_pass = False
	increase_check_pass = True
	double_only_check_pass = False

	dupe_digit_count = 0

	prev_digit = None
	current_digit = 0
	for digit in num_list:
		current_digit = current_digit + 1
		is_last_digit = current_digit == LENGTH

		if prev_digit == None:
			prev_digit = digit
			continue

		if prev_digit == digit:
			dupe_check_pass = True

			dupe_digit_count = dupe_digit_count + 1
		else:
			if dupe_digit_count == 1:
				double_only_check_pass = True

			dupe_digit_count = 0

		if is_last_digit:
			if dupe_digit_count == 1:
				double_only_check_pass = True

		if int(prev_digit) > int(digit):
			increase_check_pass = False
			break

		prev_digit = digit

	if dupe_check_pass == True and increase_check_pass == True:
		passed_number_count = passed_number_count + 1

		if double_only_check_pass == True:
			strict_passed_number_count = strict_passed_number_count + 1

print("Number of Passwords: "+str(passed_number_count))
print("Number of Passwords (Strict): "+str(strict_passed_number_count))
