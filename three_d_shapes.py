import math
import random

from mumbo_types import Config
from utils import get_random_char

X_SCALE = 0.5
Y_SCALE = 0.25


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
    global X_SCALE, Y_SCALE
    projected_vertices = []
    for vertex in vertices:
        rotated_vertex = rotate_point_3d(*vertex, angle_x, angle_y, angle_z)
        scaled_vertex = (rotated_vertex[0] * X_SCALE, rotated_vertex[1] * Y_SCALE, rotated_vertex[2] * X_SCALE)  # Scale down the shape
        projected_vertex = project_point_3d(
            *scaled_vertex, width, height, fov=256, viewer_distance=4
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
    frame, elapsed_time, current_config: Config
):
    global current_shape, is_drawing_3d_shapes

    if current_config.probability_of_turning_on_3d_shapes == 0:
        is_drawing_3d_shapes = False
    elif random.random() < (
            current_config.probability_of_turning_off_3d_shapes
            if is_drawing_3d_shapes
            else current_config.probability_of_turning_on_3d_shapes
        ):
            is_drawing_3d_shapes = not is_drawing_3d_shapes

    if not is_drawing_3d_shapes:
        return

    width = len(frame[0])
    height = len(frame)
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
        (1, 2, 1),
        (-1, -2, 1),
        (-1, 2, -1),
        (1, -2, -1),
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
        (0, 2, 0),
        (0, -2, 0),
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

    # Define vertices and edges for a dodecahedron
    dodecahedron_vertices = [
        (1, 1, 1),
        (-1, 1, 1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, -1),
        (0, (1 + 2.23606797749979) / 2, (1 + 2.23606797749979) / 2),
        (0, -(1 + 2.23606797749979) / 2, (1 + 2.23606797749979) / 2),
        (0, -(1 + 2.23606797749979) / 2, -(1 + 2.23606797749979) / 2),
        (0, (1 + 2.23606797749979) / 2, -(1 + 2.23606797749979) / 2),
        ((1 + 2.23606797749979) / 2, 0, (1 + 2.23606797749979) / 2),
        (-(1 + 2.23606797749979) / 2, 0, (1 + 2.23606797749979) / 2),
        (-(1 + 2.23606797749979) / 2, 0, -(1 + 2.23606797749979) / 2),
        ((1 + 2.23606797749979) / 2, 0, -(1 + 2.23606797749979) / 2),
        ((1 + 2.23606797749979) / 2, (1 + 2.23606797749979) / 2, 0),
        (-(1 + 2.23606797749979) / 2, (1 + 2.23606797749979) / 2, 0),
        (-(1 + 2.23606797749979) / 2, -(1 + 2.23606797749979) / 2, 0),
        ((1 + 2.23606797749979) / 2, -(1 + 2.23606797749979) / 2, 0),
        (1, 0, (1 + 2.23606797749979) / 2),
        (-1, 0, (1 + 2.23606797749979) / 2),
        (-1, 0, -(1 + 2.23606797749979) / 2),
        (1, 0, -(1 + 2.23606797749979) / 2),
        (0, (1 + 2.23606797749979) / 2, 1),
        (0, -(1 + 2.23606797749979) / 2, 1),
        (0, -(1 + 2.23606797749979) / 2, -1),
        (0, (1 + 2.23606797749979) / 2, -1),
    ]
    dodecahedron_edges = [
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
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 8),
        (12, 13),
        (13, 14),
        (14, 15),
        (15, 12),
        (8, 12),
        (9, 13),
        (10, 14),
        (11, 15),
        (16, 17),
        (17, 18),
        (18, 19),
        (19, 16),
        (20, 21),
        (21, 22),
        (22, 23),
        (23, 20),
        (16, 20),
        (17, 21),
        (18, 22),
        (19, 23),
        (8, 16),
        (9, 17),
        (10, 18),
        (11, 19),
        (12, 20),
        (13, 21),
        (14, 22),
        (15, 23),
    ]

    # Define vertices and edges for an icosahedron
    icosahedron_vertices = [
        (0, 1, 1.618033988749895),
        (0, -1, 1.618033988749895),
        (0, -1, -1.618033988749895),
        (0, 1, -1.618033988749895),
        (1.618033988749895, 0, 1),
        (-1.618033988749895, 0, 1),
        (-1.618033988749895, 0, -1),
        (1.618033988749895, 0, -1),
        (1, 1.618033988749895, 0),
        (-1, 1.618033988749895, 0),
        (-1, -1.618033988749895, 0),
        (1, -1.618033988749895, 0),
    ]
    icosahedron_edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 8),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
        (4, 8),
        (5, 9),
        (6, 10),
        (7, 11),
        (8, 0),
        (9, 1),
        (10, 2),
        (11, 3),
    ]

    shapes = [
        (cube_vertices, cube_edges),
        (tetrahedron_vertices, tetrahedron_edges),
        (octahedron_vertices, octahedron_edges),
        (dodecahedron_vertices, dodecahedron_edges),
        (icosahedron_vertices, icosahedron_edges),
    ]

    if random.random() < current_config.probability_of_changing_3d_shape:
        current_shape = random.randint(0, len(shapes) - 1)

    vertices, edges = shapes[current_shape]
    draw_shape(frame, vertices, edges, width, height, angle_x, angle_y, angle_z)
