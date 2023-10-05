https://github.com/AuracleTech/piai/assets/40531871/b0670958-27be-44ea-9f16-6185979dcf02

# Pi AI Hands Free

###### a python AI Voice Interpreter for Pi AI

## Installation

Follow these instructions _in order_ to get the application running.

1. Install requirements

- [git](https://git-scm.com/downloads)
- [FFmpeg](https://ffmpeg.org/download.html)
- [Python 3.11](https://www.python.org/downloads/release/python-3113/)

2. Clone this repository to your local machine using the following command

```shell
git clone https://github.com/AuracleTech/piai.git
```

3. Navigate to the project directory

```shell
cd piai
```

4. Install OpenAI Whisper

```shell
pip install -U openai-whisper
```

5. Install pipreqs to generates the dependencies

```shell
pip install pipreqs
```

6. Generate the dependencies file

```shell
pipreqs . --force
```

7. Install the dependencies

```shell
pip install -r requirements.txt
```

8. Launch the app

```shell
python src/main.py
```

9. Have a chat with your new voice assistant 🌟

## Development

The application uses 3 threads

1. `Recorder.py` records vocal inputs to `recordings` folder.
2. `Transcriber.py` transcribes the files and sends the transcript to the interpreter.
3. `Interpreter.py` transmits what you said to Pi.

###### OpenAI

You can use GPT to determine if Pi should respond to the vocal input, to use it follow these steps.

1. Get an [OpenAI API Key](https://openai.com/)

2. Create a .env file in the root directory and add the following variable

```shell
OPENAI_API_KEY=your-openai-api-key-here
```

3. Uncomment the code in interpreter.py and/or modify it to your liking.

## Help

Feel free to open an [issue](/issues) if you have any questions, suggestions or issues.
