import whisper
import os
import config


def transcribe(recordings_queue, transcript_queue):
    print("Transcribing...")

    MODEL = whisper.load_model("base")
    MAX_AMOUT_NO_SPEECH = 0.15

    while True:
        # Get the filepath from the queue
        filepath = recordings_queue.get()

        # If we receive exit code, stop
        if filepath == config.EXIT_CODE:
            break

        # Load audio and pad or trim to 1 second
        audio = whisper.load_audio(filepath)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(MODEL.device)
        options = whisper.DecodingOptions(
            language=config.WHISPERING_LANGUAGE, fp16=False
        )

        result = whisper.decode(MODEL, mel, options)

        if result.no_speech_prob < MAX_AMOUT_NO_SPEECH:
            print(f"{result.no_speech_prob} : {result.text}")

            # Add transcript to queue
            transcript_queue.put(result.text)

        # Delete the file
        os.remove(filepath)

    print("Stopped transcribing")
