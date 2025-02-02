import os
import random
import time


from fake_error import print_fake_error
from noisy_characters import print_noisy_characters
from three_d_shapes import print_3d_shapes
from falling_characters import print_falling_characters
from glitch_characters import print_glitch_characters
from mumbo_types import Config


current_config = Config(
    use_colors=False,
    probability_of_noisy_characters=1,
    probability_of_colour=0.1,
    probability_of_error=0.01,
    probability_of_mutating_new_glitch_characters=0.01,
    probability_of_mutating_existing_glitch_characters=0.001,
    probability_of_turning_off_colours=0.1,
    probability_of_turning_on_colours=0.01,
    probability_of_turning_off_3d_shapes=0.1,
    probability_of_turning_on_3d_shapes=0.01,
    probability_of_changing_3d_shape=0.01,
    probability_of_new_falling_character=0.03
)

is_blinking_on = False
number_of_lines_in_last_frame = 0


def main():
    global current_config, is_blinking_on, number_of_lines_in_last_frame
   
    start_time = time.time()

    while True:
        if random.random() < (
            current_config.probability_of_turning_off_colours
            if current_config.use_colors
            else current_config.probability_of_turning_on_colours
        ):
            current_config.use_colors = not current_config.use_colors

        
        is_blinking_on = not is_blinking_on

        (width, height) = os.get_terminal_size()
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # Generate empty frame
        frame = [" " * width for _ in range(height)]

        print_noisy_characters(frame, width, height, elapsed_time, current_config)
        print_3d_shapes(frame, width, height, elapsed_time, current_config)
        print_falling_characters(frame, width, height, current_config)
        print_glitch_characters(frame, width, height, current_config)
        print_fake_error(frame, width, height, current_config, is_blinking_on)

        # Clear the console
        # os.system("cls" if os.name == "nt" else "clear")

        # Empty the console's previous lines
        for _ in range(number_of_lines_in_last_frame):
            # print("\033[A\033[K", end="")
            print("\033[1A", end="\x1b[2K")

        # Render
        for line in frame:
            print(line)

        number_of_lines_in_last_frame = len(frame)

        time.sleep(0.04)


if __name__ == "__main__":
    main()
