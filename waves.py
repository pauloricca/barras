import time
from log import log
from mumbo_types import Config
import math


def print_waves(frame: list[str], current_config: Config):
    if current_config.waves_amplitude == 0 or current_config.waves_period == 0:
        return frame

    width = len(frame[0])
    height = len(frame)

    t = time.time()
    offsets = [
        int(current_config.waves_amplitude * math.sin((x + current_config.waves_speed * t) / current_config.waves_period))
        for x in range(width - 1)
        ]

    new_frame = [
        "".join(
            frame[(y + offsets[y]) % height][x]
            for x in range(width)
        )
        for y in range(height)
    ]
    
    return new_frame