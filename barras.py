from PIL import Image, ImageTk
import tkinter as tk

image_path = "image-4.jpg"
row_height = 10
animation_speed = 30


def average_color(image, x, y, size):
    pixels = image.crop((x, y, x + size, y + size)).getdata()
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)
    return (r, g, b)


def create_grid_image(image, row_height, column_position):
    width, height = image.size
    grid_image = Image.new("RGB", (width, height))
    for y in range(0, height, row_height):
        avg_color = average_color(image, column_position, y, row_height)
        grid_image.paste(avg_color, [0, y, width, y + row_height])
    return grid_image


# Open the image file
image = Image.open(image_path)

# Create a tkinter window
window = tk.Tk()
window.title("Image Display")

# Convert the image to a format tkinter can use
tk_image = ImageTk.PhotoImage(image)

# Create a label to display the image
label = tk.Label(window)
label.pack()

column_position = 0
direction = 1


# Function to update the image with the grid image
def update_image():
    global column_position, direction, row_height, animation_speed

    column_position += direction

    if column_position >= image.width:
        column_position = image.width - 1
        direction *= -1

    if column_position < 0:
        column_position = 0
        direction *= -1

    grid_image = create_grid_image(image, row_height, column_position)
    tk_grid_image = ImageTk.PhotoImage(grid_image)
    label.config(image=tk_grid_image)
    label.image = tk_grid_image
    window.after(animation_speed, update_image)


# Schedule the update_image function to run after the window is initialized
window.after(100, update_image)

# Run the tkinter event loop
window.mainloop()
