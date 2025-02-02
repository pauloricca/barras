import math
import random

from mumbo_types import Config
from utils import get_random_char


def rotate_point_3d(x, y, z, angle_x, angle_y, angle_z):
    # Rotate around x-axis
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Rotate around y-axis
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    # Rotate around z-axis
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    return x, y, z


def project_point_3d(x, y, z, width, height, fov, viewer_distance):
    factor = fov / (viewer_distance + z)
    x = x * factor + width / 2
    y = -y * factor + height / 2
    return int(x), int(y)


def draw_shape(frame, vertices, edges, width, height, angle_x, angle_y, angle_z):
    projected_vertices = []
    for vertex in vertices:
        scaled_vertex = tuple(coord * 0.25 for coord in vertex)  # Scale down the shape
        rotated_vertex = rotate_point_3d(*scaled_vertex, angle_x, angle_y, angle_z)
        projected_vertex = project_point_3d(
            *rotated_vertex, width, height, fov=256, viewer_distance=4
        )
        projected_vertices.append(projected_vertex)

    for edge in edges:
        start, end = edge
        x1, y1 = projected_vertices[start]
        x2, y2 = projected_vertices[end]
        draw_line(frame, x1, y1, x2, y2)


def draw_line(frame, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        x_inc, y_inc = 0, 0
    else:
        x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    for _ in range(steps):
        if 0 <= int(y) < len(frame) and 0 <= int(x) < len(frame[0]):
            frame[int(y)] = (
                frame[int(y)][: int(x)]
                + get_random_char()
                + frame[int(y)][int(x) + 1 :]
            )
        x += x_inc
        y += y_inc


current_shape = 0
is_drawing_3d_shapes = False


def print_3d_shapes(
    frame, width, height, elapsed_time, current_config: Config
):
    global current_shape, is_drawing_3d_shapes

    if random.random() < (
            current_config.probability_of_turning_off_3d_shapes
            if is_drawing_3d_shapes
            else current_config.probability_of_turning_on_3d_shapes
        ):
            is_drawing_3d_shapes = not is_drawing_3d_shapes

    if not is_drawing_3d_shapes:
        return

    angle_x = elapsed_time * 0.5
    angle_y = elapsed_time * 0.3
    angle_z = elapsed_time * 0.2

    # Define vertices and edges for a cube
    cube_vertices = [
        (-1, -1, -1),
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, 1, 1),
    ]
    cube_edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]

    # Define vertices and edges for a tetrahedron
    tetrahedron_vertices = [
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, -1),
        (1, -1, -1),
    ]
    tetrahedron_edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    # Define vertices and edges for an octahedron
    octahedron_vertices = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    octahedron_edges = [
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
    ]

    shapes = [
        (cube_vertices, cube_edges),
        (tetrahedron_vertices, tetrahedron_edges),
        (octahedron_vertices, octahedron_edges),
    ]

    if random.random() < current_config.probability_of_changing_3d_shape:
        current_shape = random.randint(0, len(shapes) - 1)

    vertices, edges = shapes[current_shape]
    draw_shape(frame, vertices, edges, width, height, angle_x, angle_y, angle_z)
