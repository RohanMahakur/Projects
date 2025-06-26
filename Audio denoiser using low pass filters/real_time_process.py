import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import filters
import wave
from collections import deque

# Audio settings
CHUNK = 1024
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
CUTOFF = 4000

def main():
    filter_type = 'fir'
    fir_coeffs = filters.design_fir(cutoff=CUTOFF, rate=RATE)
    b_iir, a_iir = filters.design_iir(cutoff=CUTOFF, rate=RATE)

    # Prepare audio interface
    p = pyaudio.PyAudio()

    stream_in = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

    print("🎙️  Real-Time Audio Denoiser Running...")
    print("Press 'f' for FIR, 'i' for IIR, 'q' to quit.")

    # Setup plot
    plt.ion()
    fig, ax = plt.subplots()
    x = np.arange(0, CHUNK)
    line_in, = ax.plot(x, np.random.rand(CHUNK), label='Input', alpha=0.5)
    line_out, = ax.plot(x, np.random.rand(CHUNK), label='Filtered', alpha=0.7)
    ax.set_ylim([-30000, 30000])
    ax.set_title("Real-Time Audio Waveform")
    ax.legend()

    # ✅ Buffer to store all filtered audio
    output_frames = []

    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Quitting...")
                break
            elif keyboard.is_pressed('f'):
                filter_type = 'fir'
                print("Switched to FIR filter")
            elif keyboard.is_pressed('i'):
                filter_type = 'iir'
                print("Switched to IIR filter")

            # Read audio
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Filter
            if filter_type == 'fir':
                filtered = filters.apply_fir(audio_data, fir_coeffs)
            else:
                filtered = filters.apply_iir(audio_data, b_iir, a_iir)

            # Convert and play
            filtered_int16 = np.int16(filtered)
            stream_out.write(filtered_int16.tobytes())

            # ✅ Save this chunk
            output_frames.append(filtered_int16.tobytes())

            # Update waveform
            line_in.set_ydata(audio_data)
            line_out.set_ydata(filtered_int16)
            plt.pause(0.001)

    except KeyboardInterrupt:
        print("Stopped by user.")

    # Stop streams
    stream_in.stop_stream()
    stream_out.stop_stream()
    stream_in.close()
    stream_out.close()
    p.terminate()

    plt.ioff()
    plt.close()

    # ✅ Save to WAV
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(output_frames))
    wf.close()

    print("✅ Filtered audio saved as output.wav")

if __name__ == "__main__":
    main()
