import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from filters import design_fir, apply_fir, design_iir, apply_iir

# === CONFIG ===
input_wav = 'input.wav'  # Your recorded file
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_wav = f'output_{timestamp}.wav'
plot_path = f'fft_{timestamp}.png'

cutoff = 4000  # Hz
use_fir = True  # Toggle between FIR and IIR


# === STEP 1: Load and preprocess audio ===
def load_audio(file_path):
    rate, data = wavfile.read(file_path)
    print(f"Loaded {file_path} at {rate} Hz, shape: {data.shape}")
    if data.ndim == 2:
        print("Stereo detected — converting to mono...")
        data = data.mean(axis=1).astype(np.int16)
    return rate, data


# === STEP 2: Normalize audio ===
def normalize_audio(data):
    peak = np.max(np.abs(data))
    if peak == 0:
        return data
    return (data * (32767 / peak)).astype(np.int16)


# === STEP 3: Plot FFT ===
def plot_fft(signal, rate, title, filename):
    N = len(signal)
    yf = np.abs(fft(signal))
    xf = fftfreq(N, 1 / rate)

    plt.figure(figsize=(10, 4))
    plt.plot(xf[:N // 2], yf[:N // 2])
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Frequency spectrum saved as {filename}")


# === STEP 4: Compute Noise reduction % ===
def compute_noise_reduction(original, filtered, rate, cutoff=4000):
    # Compute FFTs
    orig_fft = np.abs(fft(original))
    filt_fft = np.abs(fft(filtered))

    # Frequency bins
    freqs = fftfreq(len(orig_fft), d=1 / rate)

    # Only positive frequencies
    mask = freqs > cutoff
    orig_noise = np.sum(orig_fft[mask])
    filt_noise = np.sum(filt_fft[mask])

    # Avoid divide-by-zero
    if orig_noise == 0:
        return 0.0

    reduction = 100 * (1 - filt_noise / orig_noise)
    return reduction


# === STEP 5: Filter and save ===
def process_audio(input_wav, output_wav, plot_path, use_fir, cutoff):
    rate, data = load_audio(input_wav)

    # Plot original FFT
    plot_fft(data, rate, "Original Audio FFT", plot_path.replace(".png", "_original.png"))

    # Filter design and apply
    if use_fir:
        coeffs = design_fir(cutoff, rate)
        filtered = apply_fir(data, coeffs)
    else:
        b, a = design_iir(cutoff, rate)
        filtered = apply_iir(data, b, a)

    # Normalize and clip
    filtered = normalize_audio(filtered)
    filtered = np.clip(filtered, -32768, 32767).astype(np.int16)

    # Save to output
    wavfile.write(output_wav, rate, filtered)
    print(f"Filtered audio saved as {output_wav}")

    # Plot filtered FFT
    plot_fft(filtered, rate, "Filtered Audio FFT", plot_path.replace(".png", "_filtered.png"))
    # Compute noise reduction %
    reduction_percent = compute_noise_reduction(data, filtered, rate, cutoff=cutoff)
    # Filter summary
    print("\n=== Filter Summary ===")
    print(f"Filter type     : {'FIR' if use_fir else 'IIR'}")
    print(f"Cutoff freq     : {cutoff} Hz")
    print(f"Sample rate     : {rate} Hz")
    print(f"Audio duration  : {len(data) / rate:.2f} seconds")
    print(f"Estimated high-frequency noise reduction: {reduction_percent:.2f}%")
    print("========================\n")


# === RUN ===
if __name__ == '__main__':
    process_audio(input_wav, output_wav, plot_path, use_fir, cutoff)
