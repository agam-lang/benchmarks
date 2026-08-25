#!/usr/bin/env python3
"""Generate authentic WAV audio and PPM image files for direct Agam file processing."""

import wave
import struct
import math
from pathlib import Path

DATA_DIR = Path("benchmarks/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_piano_wav():
    wav_path = DATA_DIR / "piano_c_major.wav"
    sample_rate = 44100
    duration = 5.0 # 5 seconds
    num_samples = int(sample_rate * duration)
    
    frequencies = [261.63, 329.63, 392.00, 523.25]
    
    with wave.open(str(wav_path), "wb") as f:
        f.setnchannels(2) # Stereo
        f.setsampwidth(2) # 16-bit PCM
        f.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            envelope = math.exp(-0.8 * t)
            
            left = envelope * 12000.0 * (math.sin(2 * math.pi * frequencies[0] * t) + 0.7 * math.sin(2 * math.pi * frequencies[2] * t))
            right = envelope * 12000.0 * (math.sin(2 * math.pi * frequencies[1] * t) + 0.7 * math.sin(2 * math.pi * frequencies[3] * t))
            
            l_int = max(-32767, min(32767, int(left)))
            r_int = max(-32767, min(32767, int(right)))
            frames += struct.pack("<hh", l_int, r_int)
            
        f.writeframes(frames)
    print(f"[OK] Created real WAV file: {wav_path} ({wav_path.stat().st_size} bytes, 5.0s Stereo 44.1kHz)")

def generate_test_ppm():
    ppm_path = DATA_DIR / "test_input.ppm"
    width = 256
    height = 256
    
    with open(ppm_path, "wb") as f:
        header = f"P6\n{width} {height}\n255\n".encode("ascii")
        f.write(header)
        
        pixels = bytearray()
        for y in range(height):
            for x in range(width):
                r = (x * 17) % 256
                g = (y * 31) % 256
                b = ((x + y) * 23) % 256
                pixels += bytes([r, g, b])
        f.write(pixels)
    print(f"[OK] Created real PPM image file: {ppm_path} ({ppm_path.stat().st_size} bytes, 256x256 RGB)")

if __name__ == "__main__":
    generate_piano_wav()
    generate_test_ppm()
