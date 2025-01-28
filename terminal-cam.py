import cv2
import numpy as np

# ASCII characters used to build the output text
ASCII_CHARS = " .:=+*#@"

# Height to width ratio to adjust the aspect ratio of characters
HEIGHT_WIDTH_RATIO = 0.5


def resize_image(image, new_width=100):
    height, width = image.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * HEIGHT_WIDTH_RATIO)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


def grayify(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def pixels_to_ascii(image):
    pixels = image.flatten()
    ascii_str = "".join([ASCII_CHARS[pixel // 32] for pixel in pixels])
    return ascii_str


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_image = grayify(frame)
        resized_image = resize_image(gray_image)
        ascii_str = pixels_to_ascii(resized_image)

        img_width = resized_image.shape[1]
        ascii_img = "\n".join(
            [ascii_str[i : i + img_width] for i in range(0, len(ascii_str), img_width)]
        )

        print(ascii_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
