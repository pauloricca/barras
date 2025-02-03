
from dataclasses import dataclass

@dataclass
class Config:
    use_colors: bool = False
    noisy_characters_period: float = 5 # period of the sine function in seconds
    probability_of_noisy_characters: float = 0.5
    probability_of_colour: float = 0.1
    probability_of_error: float = 0.01
    probability_of_line_glitch: float = 0.02
    probability_of_counter_glitch: float = 0.05
    probability_of_command_glitch: float = 0.03
    probability_of_question_glitch: float = 0.01
    probability_of_character_glitch: float = 0.02
    probability_of_mutating_new_glitch_characters: float = 0.01
    probability_of_mutating_existing_glitch_characters: float = 0.001
    probability_of_turning_off_colours: float = 0.1
    probability_of_turning_on_colours: float = 0.01
    probability_of_changing_3d_shape: float = 0.01
    probability_of_turning_off_3d_shapes: float = 0.1
    probability_of_turning_on_3d_shapes: float = 0.01
    probability_of_new_falling_character: float = 0.1
