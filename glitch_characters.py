import random
import time
from commands import get_fake_command, get_question
from mumbo_types import Config
from utils import get_random_char, mutate


glitch_characters = []

def print_glitch_characters(frame, width, height, current_config: Config):
	global glitch_characters

	# Occasionally add a new glitch character
	if random.random() < 0.5:
			glitch_type = ""
			if random.random() < 0.02:
					new_glitch = get_random_char() * random.randint(20, 80)
					glitch_type = "line"
			elif random.random() < 0.05:
					new_glitch = random.randint(0, 8000000)
					glitch_type = "counter"
			elif random.random() < 0:
					new_glitch = get_fake_command()
					glitch_type = "command"
			elif random.random() < 1:
					new_glitch = get_question()
					glitch_type = "command"
			else:
					new_glitch = get_random_char()
					new_glitch = "".join(
							get_random_char() for _ in range(random.randint(1, 5))
					)
					glitch_type = "character"

			if glitch_type != "counter":
					new_glitch = mutate(
							new_glitch, current_config.probability_of_mutating_new_glitch_characters
					)

			new_x = random.randint(
					0, width - len(new_glitch) if glitch_type != "counter" else 10
			)
			new_y = random.randint(0, height - 1)
			glitch_characters.append(
					(new_glitch, (new_x, new_y), time.time_ns(), glitch_type)
			)

	# Remove old glitch characters
	glitch_characters[:] = [
			gc for gc in glitch_characters if random.random() < 0.98
	]

	# Randomly shift glitch characters coordinates
	for i in range(len(glitch_characters)):
			glitch, (x, y), birth_time, glitch_type = glitch_characters[i]
			shift_x = random.randint(-1, 1) if random.random() < 0.1 else 0
			shift_y = random.randint(-1, 1) if random.random() < 0.1 else 0
			new_x = max(0, min(width - 1, x + shift_x))
			new_y = max(0, min(height - 1, y + shift_y))
			glitch_characters[i] = (glitch, (new_x, new_y), birth_time, glitch_type)

	# Randomly swap one of the characters for a random one in glitch_characters
	for i in range(len(glitch_characters)):
			glitch, (x, y), birth_time, glitch_type = glitch_characters[i]
			if glitch_type != 'counter':
					glitch = mutate(glitch, current_config.probability_of_mutating_existing_glitch_characters)
					glitch_characters[i] = (glitch, (x, y), birth_time, glitch_type)
	
	# Add glitch characters
	for glitch, (x, y), birth_time, glitch_type in glitch_characters:
			if 0 <= y < height and 0 <= x < width:
					glitch_str = (
							glitch
							if glitch_type != "counter"
							else ":"
							+ str(int(glitch + (time.time_ns() / 1000 - birth_time / 1000)))
					)

					if glitch_type == "command":
							elapsed_time_ms = (time.time_ns() - birth_time) / 1_000_000
							max_length = min(len(glitch_str), int(elapsed_time_ms / 100))
							glitch_str = glitch_str[:max_length]
							if int(elapsed_time_ms / 50) % 2 == 0:
									glitch_str += "█"

					if current_config.use_colors or random.random() < current_config.probability_of_colour:
							glitch_str = f"\033[1;3{random.randint(1, 7)}m{glitch_str}\033[0m"

					# Ensure the glitch string does not overflow the line length
					max_length = width - x
					glitch_str = glitch_str[:max_length]
					frame[y] = frame[y][:x] + glitch_str + frame[y][x + len(glitch_str) :]
