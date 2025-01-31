import os
import random
import time
import math
import shutil


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


fixed_characters = []
glitch_characters = []
glitch_counter = 0

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
    "ssh user@host",
    "scp file user@host:/path",
    "chmod 755 script.sh",
    "chown user:group file",
    "find / -name '*.log'",
    "grep 'error' /var/log/syslog",
    "awk '{print $1}' file",
    "sed 's/foo/bar/g' file",
    "tar -czvf archive.tar.gz /path/to/dir",
    "gzip file",
    "gunzip file.gz",
    "bzip2 file",
    "bunzip2 file.bz2",
    "zip -r archive.zip /path/to/dir",
    "unzip archive.zip",
    "rsync -avz /src/ /dest/",
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
    "systemctl start service",
    "systemctl stop service",
    "systemctl restart service",
    "systemctl status service",
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
    "nmcli general status",
    "nmcli general permissions",
    "nmcli general ethernet",
    "nmcli general ip6erspan",
]

use_colors = False  # Set this to False to disable colors
probability_of_colour = 0.1  # Probability of a character being colored


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
                line += chr(random.randint(33, 126))  # Use a wider range of characters
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
            for i in range(1, 6):
                if y + i < height:
                    if use_colors or random.random() < probability_of_colour:
                        trail_char = f"\033[1;3{2};2{i * 3}3{2};2{i * 3}m{char}\033[0m"
                    else:
                        trail_char = char
                    frame[y + i] = frame[y + i][:x] + trail_char + frame[y + i][x + 1 :]

    # Add glitch characters
    for glitch, (x, y) in glitch_characters:
        if 0 <= y < height and 0 <= x < width:
            if use_colors or random.random() < probability_of_colour:
                glitch_str = f"\033[1;3{random.randint(1, 7)}m{glitch}\033[0m"
            else:
                glitch_str = glitch
            frame[y] = frame[y][:x] + glitch_str + frame[y][x + len(glitch) :]

    return frame


def main():
    global glitch_counter
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
            new_char = chr(random.randint(33, 126))  # Use a wider range of characters
            fixed_characters[i] = (new_char, (x, y + 1))

        # Remove characters that have fallen off the screen
        fixed_characters[:] = [fc for fc in fixed_characters if fc[1][1] < height]

        # Occasionally add a new fixed character
        if random.random() < 0.1:
            new_char = chr(random.randint(33, 126))  # Use a wider range of characters
            new_x = random.randint(0, width - 1)
            fixed_characters.append((new_char, (new_x, 0)))

        # Occasionally add a new glitch character
        if random.random() < 0.5:
            if random.random() < 0.1:
                new_glitch = "-" * random.randint(20, 80)
            elif random.random() < 0.3:
                new_glitch = str(glitch_counter)
                glitch_counter += 1
            elif random.random() < 0.3:
                new_glitch = random.choice(fake_commands)
            else:
                new_glitch = chr(
                    random.randint(33, 126)
                )  # Use a wider range of characters
            new_x = random.randint(0, width - len(new_glitch))
            new_y = random.randint(0, height - 1)
            glitch_characters.append((new_glitch, (new_x, new_y)))

        # Remove old glitch characters
        glitch_characters[:] = [
            gc for gc in glitch_characters if random.random() < 0.99
        ]

        time.sleep(0.04)


if __name__ == "__main__":
    main()
