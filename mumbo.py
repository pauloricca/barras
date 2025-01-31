import os
import random
import time
import math
import shutil


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


fixed_characters = []
glitch_characters = []
draw_cube = False
use_colors = False  # Set this to False to disable colors
probability_of_colour = 0.1  # Probability of a character being colored

fake_commands = [
    "ls -la",
    "cat /etc/passwd",
    "sudo rm -rf /",
    "ping 192.13.0.1",
    "ps aux",
    "top",
    "netstat -an",
    "ifconfig",
    "whoami",
    "df -h",
    "du -sh *",
    "uptime",
    "dmesg | tail",
    "free -m",
    "vmstat",
    "iostat",
    "sar -u 1 3",
    "ssh admin@huuik.com",
    "scp file user@hjs:/",
    "chmod 755 /usr/local/bin/script.sh",
    "chown user:group /var/log/file",
    "find /var/log -name '*.log'",
    "grep 'error' /var/log/syslog",
    "awk '{print $1}' /etc/hosts",
    "sed 's/foo/bar/g' /etc/hostname",
    "tar -czvf /tmp/installer.tar.gz /usr/local/share",
    "gzip /var/log/file",
    "gunzip /var/log/file.gz",
    "bzip2 /var/log/file",
    "bunzip2 /var/log/file.bz2",
    "zip -r /tmp/archive.zip /usr/local/share",
    "unzip /tmp/archive.zip",
    "rsync -avz /home/user/ /backup/user/",
    "mount /dev/sda1 /mnt",
    "umount /mnt",
    "fdisk -l",
    "mkfs.ext4 /dev/sda1",
    "useradd newuser",
    "passwd newuser",
    "usermod -aG sudo newuser",
    "userdel newuser",
    "groupadd newgroup",
    "groupdel newgroup",
    "crontab -e",
    "systemctl start apache2",
    "systemctl stop apache2",
    "systemctl restart apache2",
    "systemctl status apache2",
    "journalctl -xe",
    "hostnamectl",
    "timedatectl",
    "hwclock",
    "lsblk",
    "blkid",
    "parted /dev/sda",
    "lsof -i",
    "ss -tuln",
    "iptables -L",
    "ip link show",
    "ip addr show",
    "ip route show",
    "nmcli device status",
    "nmcli connection show",
    "nmcli connection up id 'connection_name'",
    "nmcli connection down id 'connection_name'",
    "nmcli device wifi list",
    "nmcli device wifi connect 'SSID' password 'alnc32vFS£'",
    "nmcli device wifi hotspot ifname wlan0 ssid 'SSID' password 'ljfwseSDC'",
    "nmcli radio wifi off",
    "nmcli radio wifi on",
    "who am i?",
    "does god exist?",
    "whats beyond?",
    "is there a meaning to life?",
    "is anyone listening?",
    "love me",
]


def get_random_char():
    return chr(random.randint(33, 126))


def generate_frame(width, height, empty_percentage):
    frame = []
    center_x, center_y = width // 2, height // 2
    for y in range(height):
        line = ""
        for x in range(width):
            distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            probability = 1 / (1 + distance_to_center**2)
            if random.random() < empty_percentage * (1 - probability):
                line += " "
            else:
                line += get_random_char()
        frame.append(line)

    # Add fixed characters to the frame with trails
    for char, (x, y) in fixed_characters:
        if 0 <= y < height and 0 <= x < width:
            if use_colors or random.random() < probability_of_colour:
                bold_red_char = f"\033[1;31m{char}\033[0m"
            else:
                bold_red_char = char
            frame[y] = frame[y][:x] + bold_red_char + frame[y][x + 1 :]
            # Add trails
            for i in range(1, 4):
                if y + i < height:
                    if use_colors or random.random() < probability_of_colour:
                        trail_char = f"\033[1;3{2};2{i * 3}3{2};2{i * 3}m{get_random_char()}\033[0m"
                    else:
                        trail_char = get_random_char()
                    frame[y + i] = frame[y + i][:x] + trail_char + frame[y + i][x + 1 :]

    # Add glitch characters
    for glitch, (x, y), birth_time, glitch_type in glitch_characters:
        if 0 <= y < height and 0 <= x < width:
            glitch_str = (
                glitch
                if glitch_type != "counter"
                else ":"
                + str(int(glitch + (time.time_ns() / 1000 - birth_time / 1000)))
            )

            if glitch_type == "command":
                elapsed_time_ms = (time.time_ns() - birth_time) / 1_000_000
                max_length = min(len(glitch_str), int(elapsed_time_ms / 100))
                glitch_str = glitch_str[:max_length]
                if int(elapsed_time_ms / 50) % 2 == 0:
                    glitch_str += "█"

            if use_colors or random.random() < probability_of_colour:
                glitch_str = f"\033[1;3{random.randint(1, 7)}m{glitch_str}\033[0m"
            # Ensure the glitch string does not overflow the line length
            max_length = width - x
            glitch_str = glitch_str[:max_length]
            frame[y] = frame[y][:x] + glitch_str + frame[y][x + len(glitch_str) :]

    return frame


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
            frame[int(y)] = frame[int(y)][: int(x)] + "#" + frame[int(y)][int(x) + 1 :]
        x += x_inc
        y += y_inc


def add_3d_shapes(frame, width, height, elapsed_time):
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

    draw_shape(
        frame, cube_vertices, cube_edges, width, height, angle_x, angle_y, angle_z
    )


# Add the call to add_3d_shapes in the main loop
def main():
    global draw_cube, use_colors
    period = 1  # period of the sine function in seconds
    start_time = time.time()

    while True:
        if random.random() < (0.1 if draw_cube else 0.01):
            draw_cube = not draw_cube
        if random.random() < (0.1 if use_colors else 0.01):
            use_colors = not use_colors

        (width, height) = get_terminal_size()
        current_time = time.time()
        elapsed_time = current_time - start_time
        empty_percentage = (
            (math.sin(2 * math.pi * elapsed_time / period) + 1) / 2
        ) ** 0.01

        frame = generate_frame(width, height, empty_percentage)

        if draw_cube:
            add_3d_shapes(frame, width, height, elapsed_time)

        os.system("cls" if os.name == "nt" else "clear")
        for line in frame:
            print(line)

        # Update fixed characters
        for i in range(len(fixed_characters)):
            char, (x, y) = fixed_characters[i]
            new_char = get_random_char()  # Use a wider range of characters
            fixed_characters[i] = (new_char, (x + random.randint(-1, 1), y + 1))

        # Remove characters that have fallen off the screen
        fixed_characters[:] = [fc for fc in fixed_characters if fc[1][1] < height]

        # Occasionally add a new fixed character
        if random.random() < 0.1:
            new_char = get_random_char()  # Use a wider range of characters
            new_x = random.randint(0, width - 1)
            fixed_characters.append((new_char, (new_x, 0)))

        # Occasionally add a new glitch character
        if random.random() < 0.5:
            glitch_type = ""
            if random.random() < 0.02:
                new_glitch = "-" * random.randint(20, 80)
                glitch_type = "line"
            elif random.random() < 0.1:
                new_glitch = random.randint(0, 8000000)
                glitch_type = "counter"
            elif random.random() < 0.2:
                new_glitch = random.choice(fake_commands)
                glitch_type = "command"
            else:
                new_glitch = get_random_char()
                glitch_type = "character"
            new_x = random.randint(
                0, width - len(new_glitch) if glitch_type != "counter" else 10
            )
            new_y = random.randint(0, height - 1)
            glitch_characters.append(
                (new_glitch, (new_x, new_y), time.time_ns(), glitch_type)
            )

        # Remove old glitch characters
        glitch_characters[:] = [
            gc for gc in glitch_characters if random.random() < 0.975
        ]

        # Randomly shift glitch characters coordinates
        for i in range(len(glitch_characters)):
            glitch, (x, y), birth_time, glitch_type = glitch_characters[i]
            shift_x = random.randint(-1, 1) if random.random() < 0.1 else 0
            shift_y = random.randint(-1, 1) if random.random() < 0.1 else 0
            new_x = max(0, min(width - 1, x + shift_x))
            new_y = max(0, min(height - 1, y + shift_y))
            glitch_characters[i] = (glitch, (new_x, new_y), birth_time, glitch_type)

        # Randomly swap one of the characters for a random one in glitch_characters
        if glitch_characters and random.random() < 0.1:
            index = random.randint(0, len(glitch_characters) - 1)
            glitch, (x, y), birth_time, glitch_type = glitch_characters[index]
            if glitch_type != "counter":
                new_char = get_random_char()
                glitch_characters[index] = (new_char, (x, y), birth_time, glitch_type)

        time.sleep(0.04)


if __name__ == "__main__":
    main()
