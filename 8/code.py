IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
WIDTH_HEIGHT = IMAGE_WIDTH * IMAGE_HEIGHT

with open("input.txt") as image_file:
	image_data = [int(i) for i in image_file.read()]

image_layers = []
for i in range(len(image_data)//WIDTH_HEIGHT):
	idx = i * WIDTH_HEIGHT
	image_layers.append(image_data[ idx : idx+WIDTH_HEIGHT ])

#Validate image
fewest_zeros = 99999999999
fewest_zeros_layer = 0

layer_digit_counts = []

for layer in range(len(image_layers)):

	number_counting_map = [0,0,0,0,0,0,0,0,0,0]

	for number in image_layers[layer]:
		number_counting_map[number] = number_counting_map[number] + 1

	layer_digit_counts.append(number_counting_map)

	if number_counting_map[0] < fewest_zeros:
		fewest_zeros = number_counting_map[0]
		fewest_zeros_layer = layer

ones_mul_twos = layer_digit_counts[fewest_zeros_layer][1] * layer_digit_counts[fewest_zeros_layer][2]

print("Fewest Zeros Layer: " + str(fewest_zeros_layer))
print("1 * 2 For that Layer: " + str(ones_mul_twos))

#Render image
final_image = image_layers[0]

for layer in range(len(image_layers)):
	for i, pixel in enumerate(image_layers[layer]):
		if final_image[i] == 2:
			final_image[i] = pixel

from PIL import Image
img = Image.new( 'RGB', (IMAGE_WIDTH,IMAGE_HEIGHT), "green")
pixels = img.load() 

for i, pixel in enumerate(final_image):
	pixels[(i%IMAGE_WIDTH), (i//IMAGE_WIDTH)] = (pixel*255, pixel*255, pixel*255)

img.save("output.png")
print("Decoded image saved, check Output.png")