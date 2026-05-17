import numpy as np

def warmup_vad_model(model, num_warmup_chunks=10):
    """
    Pre-warm Silero VAD model with silent audio chunks.
    This prevents cold-start latency on first speech detection.
    """
    dummy_audio = np.zeros(512, dtype=np.float32)
    dummy_state = np.zeros((2, 1, 128), dtype=np.float32)
    
    for _ in range(num_warmup_chunks):
        inputs = {
            "input": np.expand_dims(dummy_audio, axis=0),
            "sr": np.array([16000], dtype=np.int64),
            "state": dummy_state
        }
        _, dummy_state = model.run(None, inputs)
    
    return dummy_state
