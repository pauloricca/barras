import random
from mumbo_types import Config
from utils import get_random_char

falling_characters = []


def print_falling_characters(frame, width, height, current_config: Config):
	global falling_characters
					
	# Update falling characters
	for i in range(len(falling_characters)):
			char, (x, y) = falling_characters[i]
			new_char = get_random_char()  # Use a wider range of characters
			falling_characters[i] = (new_char, (x + random.randint(-1, 1), y + 1))

	# Remove characters that have fallen off the screen
	falling_characters[:] = [fc for fc in falling_characters if fc[1][1] < height]

	# Occasionally add a new falling character
	if random.random() < current_config.probability_of_new_falling_character:
			new_char = get_random_char()  # Use a wider range of characters
			new_x = random.randint(0, width - 1)
			falling_characters.append((new_char, (new_x, 0)))

	# Add falling characters to the frame with trails
	for char, (x, y) in falling_characters:
			if 0 <= y < height and 0 <= x < width:
					if (
							current_config.use_colors
							or random.random() < current_config.probability_of_colour
					):
							bold_red_char = f"\033[1;31m{char}\033[0m"
					else:
							bold_red_char = char
					frame[y] = frame[y][:x] + bold_red_char + frame[y][x + 1 :]

					# Add trails
					for i in range(1, 4):
							if y + i < height:
									if (
											current_config.use_colors
											or random.random() < current_config.probability_of_colour
									):
											trail_char = f"\033[1;3{2};2{i * 3}3{2};2{i * 3}m{get_random_char()}\033[0m"
									else:
											trail_char = get_random_char()
									frame[y + i] = frame[y + i][:x] + trail_char + frame[y + i][x + 1 :]

