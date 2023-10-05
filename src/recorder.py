import pyaudio
import librosa
import numpy as np
import datetime
import os
import wave


def listen(recordings_path, recordings_queue):
    # Matching whisper settings
    FORMAT = pyaudio.paInt16
    # OpenAI whisper uses 1 channel by default
    CHANNELS = 1
    # OpenAI whisper uses 16kHz sample rate by default
    RATE = 16000  # HARD CODED IN WHISPER
    # Amount of frames per second
    FRAME_PER_SEC = 40
    # Proportion of the frame required to be considered silent (0.0 - 1.0)
    FRAME_SILENCE_THRESHOLD = 0.9
    # Silence RMS ceiling
    SILENCE_RMS_CEILING = 64
    # Frame length in bytes
    RATE_PER_FRAME = RATE // FRAME_PER_SEC
    # Amount of rate before silence
    RATE_BEFORE_SILENCE = FRAME_SILENCE_THRESHOLD * FRAME_PER_SEC

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open microphone stream
    print("Listening...")
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=RATE_PER_FRAME,
    )

    print("Press ctrl + c to stop")
    while True:
        frames = []
        consecutive_silent_frames = 0

        while True:
            # Read audio data from the stream
            data = stream.read(RATE_PER_FRAME)
            frames.append(data)

            # Check for silence
            chunk = np.frombuffer(data, dtype=np.int16)
            rms_features = librosa.feature.rms(
                y=chunk, frame_length=RATE_PER_FRAME, hop_length=RATE_PER_FRAME
            )
            rms = np.average(rms_features)

            # Verify the current frame is silent
            if rms < SILENCE_RMS_CEILING:
                consecutive_silent_frames += 1
            else:
                consecutive_silent_frames = 0

            # If there are consecutive silent frames, stop recording
            if consecutive_silent_frames > RATE_BEFORE_SILENCE:
                break

        # If all frames are silent, skip saving the file
        if len(frames) == consecutive_silent_frames:
            continue

        # Save the recorded audio to a WAV file
        timestamp = datetime.datetime.now().timestamp()
        filename = f"{timestamp}.wav"
        filepath = os.path.join(recordings_path, filename)

        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))

        # Add file path to queue
        recordings_queue.put(filepath)

    # Close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Stopped listening")
