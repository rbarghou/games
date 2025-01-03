import numpy as np
from array import array
from pygame import mixer

SAMPLE_RATE = 44100

def generate_sine_wave(frequency, duration, volume=0.5):
    num_samples = int(SAMPLE_RATE * duration)
    samples = np.arange(num_samples)
    wave = np.sin(2 * np.pi * frequency * samples / SAMPLE_RATE)
    wave = (wave * volume * 32767).astype(np.int16)
    return array('h', wave)

class SoundManager:
    def __init__(self):
        mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
        self.match_sound = self._create_match_sound()
        self.fail_sound = self._create_fail_sound()
        self.lose_life_sound = self._create_lose_life_sound()
        self.combo_sound = self._create_combo_sound()

    def _create_match_sound(self):
        sound_data = generate_sine_wave(440, 0.1)
        sound_data.extend(generate_sine_wave(554.37, 0.1))
        sound_data.extend(generate_sine_wave(659.25, 0.1))
        return mixer.Sound(buffer=sound_data)

    def _create_fail_sound(self):
        sound_data = generate_sine_wave(440, 0.1)
        sound_data.extend(generate_sine_wave(415.30, 0.2))
        return mixer.Sound(buffer=sound_data)

    def _create_lose_life_sound(self):
        return mixer.Sound(buffer=generate_sine_wave(220, 0.3, 0.7))

    def _create_combo_sound(self):
        sound_data = generate_sine_wave(440, 0.1)
        sound_data.extend(generate_sine_wave(659.25, 0.1))
        sound_data.extend(generate_sine_wave(880, 0.2))
        return mixer.Sound(buffer=sound_data)