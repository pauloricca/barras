import os
import random
import time
import math
import shutil


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


fixed_characters = []


def generate_frame(width, height, empty_percentage):
    frame = []
    center_x, center_y = width // 2, height // 2
    for y in range(height):
        line = ""
        for x in range(width):
            distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            probability = 1 / (1 + distance_to_center**1.5)
            if random.random() < empty_percentage * (1 - probability):
                line += " "
            else:
                line += chr(random.randint(33, 120))
        frame.append(line)

    # Add fixed characters to the frame with trails
    for char, (x, y) in fixed_characters:
        if 0 <= y < height and 0 <= x < width:
            bold_green_char = f"\033[1;32m{char}\033[0m"
            frame[y] = frame[y][:x] + bold_green_char + frame[y][x + 1 :]
            # Add trails
            for i in range(1, 6):
                if y + i < height:
                    # trail_char = f"\033[1;3{2};2{8 - i}3{2};2{8 - i}m{char}\033[0m"
                    trail_char = (
                        f"\033[1;3{2};2{8 - i * 3}3{2};2{8 - i * 3}m{char}\033[0m"
                    )
                    # trail_char = f"\033[1;3{2};2{8 - i}m{char}\033[0m"
                    frame[y + i] = frame[y + i][:x] + trail_char + frame[y + i][x + 1 :]

    return frame


def main():
    period = 1  # period of the sine function in seconds
    start_time = time.time()

    while True:
        (width, height) = get_terminal_size()
        current_time = time.time()
        elapsed_time = current_time - start_time
        empty_percentage = (
            (math.sin(2 * math.pi * elapsed_time / period) + 1) / 2
        ) ** 0.01

        frame = generate_frame(width, height, empty_percentage)

        os.system("cls" if os.name == "nt" else "clear")
        for line in frame:
            print(line)

        # Update fixed characters
        for i in range(len(fixed_characters)):
            char, (x, y) = fixed_characters[i]
            new_char = chr(random.randint(33, 120))
            fixed_characters[i] = (new_char, (x, y + 1))

        # Remove characters that have fallen off the screen
        fixed_characters[:] = [fc for fc in fixed_characters if fc[1][1] < height]

        # Occasionally add a new fixed character
        if random.random() < 0.3:
            new_char = chr(random.randint(33, 120))
            new_x = random.randint(0, width - 1)
            fixed_characters.append((new_char, (new_x, 0)))

        time.sleep(0.04)


if __name__ == "__main__":
    main()
