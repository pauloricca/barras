from copy import copy
import os
import random
import time

from fake_error import print_fake_error
from noisy_characters import print_noisy_characters
from tetris import print_tetris
from three_d_shapes import print_3d_shapes
from falling_characters import print_falling_characters
from glitch_characters import print_glitch_characters
from mumbo_types import Config
from log import log
from waves import print_waves

START_STAGE = 2

stages: list[Config] = [
    Config(
        transition_time=3,
        duration=15,
        print_glitches_at_bottom_of_frame=True,
        probability_of_command_glitch=0.02,
    ),
    Config(
        transition_time=8,
        duration=25,
        print_glitches_at_bottom_of_frame=True,
        probability_of_command_glitch=0.01,
        probability_of_question_glitch=0.005,
        probability_of_turning_off_colours=0.5,
        probability_of_turning_on_colours=0.005,
        probability_of_mutating_new_glitch_characters=0.01,
        probability_of_new_tetris_piece=0.01,
    ),
    Config(
        transition_time=15,
        duration=30,
        use_colors=False,
        noisy_characters_period=5,
        probability_of_noisy_characters=1,
        probability_of_colour=0.1,
        probability_of_error=0.01,
        probability_of_line_glitch=0.02,
        probability_of_counter_glitch=0.05,
        probability_of_command_glitch=0.03,
        probability_of_question_glitch=0.01,
        probability_of_character_glitch=0.02,
        probability_of_mutating_new_glitch_characters=0.01,
        probability_of_mutating_existing_glitch_characters=0.001,
        probability_of_turning_off_colours=0.1,
        probability_of_turning_on_colours=0.01,
        probability_of_turning_off_3d_shapes=0.1,
        probability_of_turning_on_3d_shapes=1.0,
        probability_of_changing_3d_shape=0.01,
        probability_of_new_falling_character=0.03,
        probability_of_new_tetris_piece=0.05,
        puzzle_piece_scale_probability_weights=[1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5],
        waves_period=5,
        waves_amplitude=10,
        waves_speed=0.5,
    )
]



current_config_index = START_STAGE
current_config = copy(stages[current_config_index])
previous_config = stages[current_config_index]
last_transition_time = time.time()
has_finished_transition = False
is_blinking_on = False
number_of_lines_in_last_frame = 0


def main():
    global current_config, is_blinking_on, number_of_lines_in_last_frame, current_config_index, previous_config, last_transition_time, has_finished_transition

    start_time = time.time()

    while True:
        current_time = time.time()

        if current_time - last_transition_time >= current_config.duration:
            previous_config = stages[current_config_index]
            current_config_index = (current_config_index + 1) % len(stages)
            last_transition_time = current_time
            has_finished_transition = False

        if current_time - last_transition_time < current_config.transition_time:
            elapsed_transition_time = current_time - last_transition_time
            transition_progress = elapsed_transition_time / current_config.transition_time

            for attr in dir(current_config):
                if not attr.startswith("__") and not isinstance(getattr(current_config, attr), bool) and isinstance(getattr(current_config, attr), (int, float)):
                    target_value = getattr(stages[current_config_index], attr)
                    previous_value = getattr(previous_config, attr)
                    interpolated_value = previous_value + (target_value - previous_value) * transition_progress
                    setattr(current_config, attr, interpolated_value)
        elif not has_finished_transition:
            current_config = copy(stages[current_config_index])
            log("transtion complete")
            has_finished_transition = True

        if random.random() < (
            current_config.probability_of_turning_off_colours
            if current_config.use_colors
            else current_config.probability_of_turning_on_colours
        ):
            current_config.use_colors = not current_config.use_colors

        is_blinking_on = not is_blinking_on

        (width, height) = os.get_terminal_size()
        elapsed_time = current_time - start_time

        # Generate empty frame
        frame = [" " * width for _ in range(height)]

        print_noisy_characters(frame, elapsed_time, current_config)
        print_3d_shapes(frame, elapsed_time, current_config)
        print_tetris(frame, current_config)
        print_falling_characters(frame, current_config)
        print_glitch_characters(frame, current_config)
        print_fake_error(frame, current_config, is_blinking_on)

        # limit the frame to the console's width
        frame = [line[:width] for line in frame]
        frame = print_waves(frame, current_config)

        # Clear the console
        os.system("cls" if os.name == "nt" else "clear")

        # Empty the console's previous lines
        # for _ in range(number_of_lines_in_last_frame):
            ## print("\033[A\033[K", end="")
            # print("\033[1A", end="\x1b[2K")

        # Render
        for line in frame:
            print(line)

        number_of_lines_in_last_frame = len(frame)

        time.sleep(0.04)


if __name__ == "__main__":
    main()
