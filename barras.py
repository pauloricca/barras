import argparse
from PIL import Image, ImageTk
import tkinter as tk
import cv2
import numpy as np

# Command line argument parsing
parser = argparse.ArgumentParser(description="Image display with grid animation.")
parser.add_argument(
    "image_path", nargs="?", default="image.jpg", help="Path to the image file."
)
parser.add_argument(
    "-c",
    "--camera",
    action="store_true",
    help="Use the webcam instead of an image file.",
)
args = parser.parse_args()

image_path = args.image_path
row_height = 10
animation_speed = 0.1
animation_interval = 15
use_camera = args.camera


def average_color(image, x, y, size):
    pixels = np.array(image.crop((x, y, x + size, y + size)))
    avg_color = pixels.mean(axis=(0, 1)).astype(int)
    return tuple(avg_color)


def create_grid_image(image, row_height, column_position):
    width, height = image.size
    grid_image = Image.new("RGB", (width, height))
    for y in range(0, height, row_height):
        avg_color = average_color(image, column_position, y, row_height)
        grid_image.paste(avg_color, [0, y, width, y + row_height])
    return grid_image


# Open the image file or capture from webcam
if use_camera:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        raise Exception("Could not read from webcam")
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
else:
    image = Image.open(image_path)

# Create a tkinter window
window = tk.Tk()
window.title("Image Display")

# Set the initial size of the window to match the image dimensions
window.geometry(f"{image.width}x{image.height}")

# Ensure the window gets focus on start
window.focus_force()

# Convert the image to a format tkinter can use
tk_image = ImageTk.PhotoImage(image)

# Create a label to display the image
label = tk.Label(window)
label.pack(fill=tk.BOTH)

column_position = 0.0
direction = 1
is_fullscreen = False

# Precompute the average colors for each column if not using camera
if not use_camera:
    width, height = image.size
    avg_colors = np.zeros(
        (width, (height + row_height - 1) // row_height, 3), dtype=int
    )
    for x in range(width):
        for y in range(0, height, row_height):
            avg_colors[x, y // row_height] = average_color(image, x, y, row_height)


# Function to update the image with the grid image
def update_image():
    global column_position, direction, row_height, animation_interval, image, animation_speed

    if use_camera:
        ret, frame = cap.read()
        if ret:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    column_position += direction * animation_speed

    if column_position >= image.width:
        column_position = image.width - 1
        direction *= -1

    if column_position < 0:
        column_position = 0
        direction *= -1

    col_floor = int(column_position)
    col_ceil = min(col_floor + 1, image.width - 1)
    blend_factor = column_position - col_floor

    width, height = image.size
    grid_image = Image.new("RGB", (width, height))
    for y in range(0, height, row_height):
        if use_camera:
            avg_color_floor = average_color(image, col_floor, y, row_height)
            avg_color_ceil = average_color(image, col_ceil, y, row_height)
        else:
            avg_color_floor = avg_colors[col_floor, y // row_height]
            avg_color_ceil = avg_colors[col_ceil, y // row_height]
        blended_color = tuple(
            int(
                avg_color_floor[i] * (1 - blend_factor)
                + avg_color_ceil[i] * blend_factor
            )
            for i in range(3)
        )
        grid_image.paste(blended_color, [0, y, width, y + row_height])

    grid_image = grid_image.resize((window.winfo_width(), window.winfo_height()))
    tk_grid_image = ImageTk.PhotoImage(grid_image)
    label.config(image=tk_grid_image)
    label.image = tk_grid_image
    window.after(animation_interval, update_image)


def toggle_fullscreen(event=None):
    global is_fullscreen

    if not is_fullscreen:
        window.config(cursor="none")
        window.attributes("-fullscreen", True)
        window.attributes("-topmost", True)
    else:
        window.config(cursor="")
        window.attributes("-fullscreen", False)
        window.attributes("-topmost", False)
    is_fullscreen = not is_fullscreen


def quit(event=None):
    window.quit()


def increase_row_height(event=None):
    global row_height
    row_height += 1


def decrease_row_height(event=None):
    global row_height
    if row_height > 1:
        row_height -= 1


def increase_animation_speed(event=None):
    global animation_speed
    animation_speed *= 2


def decrease_animation_speed(event=None):
    global animation_speed
    animation_speed /= 2


# Bind the F key to toggle fullscreen, Esc key to quit, Up key to increase row height, and Down key to decrease row height
window.bind("<F>", toggle_fullscreen)
window.bind("<f>", toggle_fullscreen)
window.bind("<Escape>", quit)
window.bind("<Up>", increase_row_height)
window.bind("<Down>", decrease_row_height)
window.bind("<Right>", increase_animation_speed)
window.bind("<Left>", decrease_animation_speed)

# Schedule the update_image function to run after the window is initialized
window.after(100, update_image)

# Run the tkinter event loop
window.mainloop()

if use_camera:
    cap.release()
