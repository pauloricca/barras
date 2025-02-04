import random
from mumbo_types import Config
from utils import get_random_char

tetris_pieces = []
frames_per_movement = 5
probability_of_tetris_piece_rotating = 0.1
probability_of_tetris_piece_moving_sideways = 0.3
probability_of_tetris_piece_dropping = 0.01

def print_tetris(frame, current_config: Config):
    global tetris_pieces, frames_per_movement, probability_of_tetris_piece_rotating, probability_of_tetris_piece_dropping, probability_of_tetris_piece_moving_sideways

    width = len(frame[0])
    height = len(frame)

    # Update pieces
    for i in range(len(tetris_pieces)):
        piece, (x, y), rotation, is_dropping, frames_since_last_movement, character, scale = tetris_pieces[i]
        if random.random() < probability_of_tetris_piece_rotating:
            rotation = (rotation + random.randint(-1, 1)) % 4

        if random.random() < probability_of_tetris_piece_moving_sideways:
            x += random.choice([-1, 1]) * scale
        
        if random.random() < probability_of_tetris_piece_dropping:
            is_dropping = True

        if is_dropping:
            y += 2 * scale
        else:
            frames_since_last_movement += 1
            if frames_since_last_movement == frames_per_movement:
                y += 1 * scale
                frames_since_last_movement = 0
    
        tetris_pieces[i] = (piece, (x, y), rotation, is_dropping, frames_since_last_movement, character, scale)

    # Remove pieces that have reached the bottom of the screen
    tetris_pieces[:] = [fp for fp in tetris_pieces if fp[1][1] < height]

    # Occasionally add a new falling piece
    if random.random() < current_config.probability_of_new_tetris_piece:
        new_piece = get_random_piece()  # Use a wider range of tetris pieces
        new_x = random.randint(0, width - 1)
        tetris_pieces.append((new_piece, (new_x, 0), 0, False, 0, get_random_char(), random.choice(current_config.puzzle_piece_scale_probability_weights)))


    # Add falling pieces to the frame
    for piece, (x, y), rotation, is_dropping, frames_since_last_movement, character, scale in tetris_pieces:
        if 0 <= y < height and 0 <= x < width:
            draw_piece(frame, piece, x, y, rotation, current_config.use_colors, get_random_char(), scale)



def get_random_piece():
    # Return a random tetris piece
    pieces = [
        [
            "  X ",
            "  X ",
            "  X ",
            "  X "
        ],
        [
            " X  ",
            " X  ",
            " XX ",
            "    "
        ],
        [
            " X  ",
            " X  ",
            "  XX",
            "    "
        ],
        [
            "    ",
            " XX ",
            " XX ",
            "    "
        ],
        [
            " X  ",
            " XX ",
            " X  ",
            "    "
        ],
        [
            " X  ",
            " XX ",
            "  X ",
            "    "
        ],
        [
            "    ",
            "XXX ",
            " X  ",
            "    "
        ]
    ]
    return random.choice(pieces)


def draw_piece(frame, piece, x, y, rotation, use_colors, character, scale=1):
    # Rotate the piece
    for _ in range(rotation):
        piece = rotate_piece(piece)

    # Draw the tetris piece on the frame
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == "X":
                for k in range(scale):
                    for l in range(scale):
                        if 0 <= y + i*scale + k < len(frame) and 0 <= x + j*scale + l < len(frame[0]):
                            if use_colors:
                                frame[y + i*scale + k] = frame[y + i*scale + k][:x + j*scale + l] + "\033[1;31m" + character + "\033[0m" + frame[y + i*scale + k][x + j*scale + l + 1:]
                            else:
                                frame[y + i*scale + k] = frame[y + i*scale + k][:x + j*scale + l] + character + frame[y + i*scale + k][x + j*scale + l + 1:]


def rotate_piece(piece):
    # Rotate the tetris piece
    return list(map("".join, zip(*reversed(piece))))
