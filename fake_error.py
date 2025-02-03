import random

from commands import get_fake_command
from mumbo_types import Config
from utils import get_random_char, mutate


fake_error = []
fake_error_x = 0
fake_error_y = 0
fake_error_frames_remaining = 0

def get_fake_error(probability_of_reading_file=0.1, probability_of_mutating_characters=0):
    error_types = [
        [
            "Traceback (most recent call last):",
            f'  File "/Users/pauloricca/Desktop/projects/barras/mumbo.py", line {random.randint(10, 200)}, in <module>',
            f"    {random.choice(get_fake_command())}",
            f"{random.choice(['NameError', 'TypeError', 'ValueError', 'AttributeError'])}: {random.choice(['name', 'type', 'value', 'attribute'])} '{get_random_char()}' is not defined",
        ],
        [
            'Exception in thread "main" java.lang.NullPointerException',
            f"\tat {random.choice(['com.example.Main.main', 'com.example.Helper.process', 'com.example.Service.run'])}({random.choice(['Main.java', 'Helper.java', 'Service.java'])}:{random.randint(10, 200)})",
        ],
        [
            "Unhandled Exception: System.NullReferenceException",
            f"   at {random.choice(['Example.Program.Main', 'Example.Helper.Process', 'Example.Service.Run'])}() in {random.choice(['Program.cs', 'Helper.cs', 'Service.cs'])}:line {random.randint(10, 200)}",
        ],
        [
            "SyntaxError: unexpected EOF while parsing",
            f'  File "/Users/pauloricca/Desktop/projects/barras/mumbo.py", line {random.randint(10, 200)}',
        ],
        [
            "Segmentation fault (core dumped)",
            f"    at {random.choice(['main', 'function', 'process'])}() in {random.choice(['program.c', 'module.c', 'service.c'])}:{random.randint(10, 200)}",
        ],
        [
            "Bus error (core dumped)",
            f"    at {random.choice(['main', 'function', 'process'])}() in {random.choice(['program.c', 'module.c', 'service.c'])}:{random.randint(10, 200)}",
        ],
        [
            "COBOL runtime error",
            f"    at {random.choice(['PROCEDURE DIVISION', 'DATA DIVISION', 'ENVIRONMENT DIVISION'])} in {random.choice(['program.cbl', 'module.cbl', 'service.cbl'])} line {random.randint(10, 200)}",
        ],
        [
            "COBOL syntax error",
            f"    at {random.choice(['PROCEDURE DIVISION', 'DATA DIVISION', 'ENVIRONMENT DIVISION'])} in {random.choice(['program.cbl', 'module.cbl', 'service.cbl'])} line {random.randint(10, 200)}",
        ],
    ]

    # Randomly open this file and read a few lines to use as the error message, or pick a random error type
    if random.random() < probability_of_reading_file:
        with open(__file__, "r") as f:
            lines = f.readlines()
            start_line = random.randint(0, len(lines) - 6)
            num_lines = random.randint(3, 6)
            error = lines[start_line : start_line + num_lines]
            error = [line.strip() for line in error]
    else:
        error = random.choice(error_types)

    error = mutate(error, probability_of_mutating_characters)

    return error


def print_fake_error(frame, current_config: Config, is_blinking_on):
	global fake_error, fake_error_x, fake_error_y, fake_error_frames_remaining

	width = len(frame[0])
	height = len(frame)
	
	if random.random() < current_config.probability_of_error and fake_error_frames_remaining <= 0:
			fake_error = get_fake_error()
			fake_error_y = random.randint(0, max(0, height - len(fake_error)))
			fake_error_x = random.randint(
					0, max(0, width - max(len(line) for line in fake_error))
			)
			fake_error_frames_remaining = random.randint(5, 50)

	if fake_error_frames_remaining > 0:
			if random.random() < 0.1:
					fake_error_x = max(0, min(width - 1, fake_error_x + random.randint(-1, 1)))
					fake_error_y = max(0, min(height - 1, fake_error_y + random.randint(-1, 1)))
			for i, line in enumerate(fake_error):
					if is_blinking_on and fake_error_y + i < height:
							frame[fake_error_y + i] = (
									frame[fake_error_y + i][:fake_error_x]
									+ line
									+ frame[fake_error_y + i][fake_error_x + len(line) :]
							)
					fake_error_frames_remaining -= 1
