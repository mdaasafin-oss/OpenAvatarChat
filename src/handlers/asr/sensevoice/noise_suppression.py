import numpy as np

def reduce_noise(audio: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
    """
    Simple spectral subtraction noise suppression.
    Estimates noise from the first 0.1 seconds and subtracts it.
    """
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32)

    n_fft = 512
    hop_length = 256
    noise_sample_len = int(sample_rate * 0.1)

    if len(audio) < noise_sample_len:
        return audio

    # Estimate noise profile from first 0.1 seconds
    noise_sample = audio[:noise_sample_len]
    noise_fft = np.fft.rfft(noise_sample, n=n_fft)
    noise_power = np.abs(noise_fft) ** 2

    # Process full audio in frames
    frames = []
    for start in range(0, len(audio) - n_fft, hop_length):
        frame = audio[start:start + n_fft]
        frame_fft = np.fft.rfft(frame)
        frame_power = np.abs(frame_fft) ** 2
        frame_phase = np.angle(frame_fft)

        # Spectral subtraction
        clean_power = np.maximum(frame_power - noise_power, 0.01 * frame_power)
        clean_magnitude = np.sqrt(clean_power)
        clean_fft = clean_magnitude * np.exp(1j * frame_phase)
        clean_frame = np.fft.irfft(clean_fft)
        frames.append(clean_frame[:hop_length])

    if not frames:
        return audio

    return np.concatenate(frames).astype(np.float32)
