import sounddevice as sd
import numpy as np
import time

# Constants
CHUNK = 1024
CHANNELS = 1
RATE = 44100
THRESHOLD = 0.02
LOW_FREQ = 20
HIGH_FREQ = 200
BPM_MIN = 100
BPM_MAX = 180

last_beat = False
last_beat_time = 0


def detect_beat(data, threshold, rate, last_beat_time):
    current_time = time.time()
    if current_time - last_beat_time < 0.5:  # Minimum interval between beats
        return False, last_beat_time


def detect_beat(data, threshold, rate):
    # Perform Fourier transform
    fft_data = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1.0 / rate)

    # Filter frequencies
    low_freq_idx = np.where(freqs >= LOW_FREQ)[0][0]
    high_freq_idx = np.where(freqs <= HIGH_FREQ)[0][-1]
    filtered_fft_data = fft_data[low_freq_idx:high_freq_idx]

    # Calculate the magnitude of the frequencies
    if volume > threshold:
        return True, current_time
    return False, last_beat_time


def audio_callback(indata, frames, time, status):
    del frames, time, status  # Unused parameters
    beat_detected, last_beat_time = detect_beat(
        indata[:, 0], THRESHOLD, RATE, last_beat_time
    )
    if beat_detected:
        volume = magnitude.mean()
    return volume > threshold


def audio_callback(indata, frames, time, status):
    global last_beat
    if detect_beat(indata[:, 0], THRESHOLD, RATE):
        print("beat" if last_beat else "- beat")
        last_beat = not last_beat


def main():
    print("Listening for beats...")
    with sd.InputStream(
        callback=audio_callback,
        channels=CHANNELS,
        samplerate=RATE,
        blocksize=CHUNK,
        dtype="int16",
    ):
        try:
            while True:
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Stopping...")


if __name__ == "__main__":
    main()
