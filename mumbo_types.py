
from dataclasses import dataclass, field
from typing import List

def default_puzzle_piece_scale_probability_weights() -> List[float]:
    return [1]

@dataclass
class Config:
    transition_time: float = 1 # time in seconds it takes to transition to this config
    duration: float = 0 # time in seconds to stay in this config
    use_colors: bool = False
    noisy_characters_period: float = 5 # period of the sine function in seconds
    probability_of_noisy_characters: float = 0
    probability_of_colour: float = 0
    probability_of_error: float = 0
    print_glitches_at_bottom_of_frame: bool = False # When true, glitches appear like a normal console
    probability_of_line_glitch: float = 0
    probability_of_counter_glitch: float = 0
    probability_of_command_glitch: float = 0
    probability_of_question_glitch: float = 0
    probability_of_character_glitch: float = 0
    probability_of_mutating_new_glitch_characters: float = 0
    probability_of_mutating_existing_glitch_characters: float = 0
    probability_of_turning_off_colours: float = 0
    probability_of_turning_on_colours: float = 0
    probability_of_changing_3d_shape: float = 0
    probability_of_turning_off_3d_shapes: float = 0
    probability_of_turning_on_3d_shapes: float = 0
    probability_of_new_falling_character: float = 0
    probability_of_new_tetris_piece: float = 0
    puzzle_piece_scale_probability_weights: List[float] = field(default_factory=default_puzzle_piece_scale_probability_weights)
    waves_period: float = 0
    waves_amplitude: float = 0
    waves_speed: float = 0




    
