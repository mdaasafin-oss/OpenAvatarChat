## Barge-in (Interrupt) Fix

The VAD handler already supports barge-in detection via the `POST_END` 
monitoring state and `input_enabled` flag.

Key fix: In simplex mode, when the chatbot is speaking (CLIENT_PLAYBACK 
STREAM_BEGIN), VAD disables input. When user speaks during this period, 
the signal CLIENT_PLAYBACK STREAM_END re-enables VAD immediately.

The `reconnect_threshold_samples` parameter (default=8000) controls how 
quickly a user can interrupt. Reduced to 4000 for faster interrupt response.
