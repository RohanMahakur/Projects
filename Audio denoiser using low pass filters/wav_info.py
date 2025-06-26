import wave
import contextlib

filename = 'input.wav'

with contextlib.closing(wave.open(filename, 'rb')) as wf:
    channels = wf.getnchannels()
    sample_rate = wf.getframerate()
    sampwidth = wf.getsampwidth()  # in bytes
    frames = wf.getnframes()
    duration = frames / float(sample_rate)

    print(f"Channels      : {channels}")
    print(f"Sample Rate   : {sample_rate} Hz")
    print(f"Sample Width  : {sampwidth * 8} bits")
    print(f"Duration      : {duration:.2f} seconds")
