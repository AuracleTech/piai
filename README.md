https://github.com/AuracleTech/piai/assets/40531871/b0670958-27be-44ea-9f16-6185979dcf02

# Hands Free Pi AI

###### a python AI Voice Command Assistant

Three agents working in parallel

1. The **Recorder** which records vocal inputs and saves them to the recordings folder.
2. A **Transcriber** which transcribes the recordings and passes them to the interpreter.
3. An **Interpreter** which interprets the transcribed questions and passes the results to the browser.

## Usage

Follow these instructions _in order_ to get the application running.

1. Install requirements

- [git](https://git-scm.com/downloads)
- [FFmpeg](https://ffmpeg.org/download.html)
- [Python 3.11](https://www.python.org/downloads/release/python-3113/)
- [OpenAI API Key](https://openai.com/) (Optional, see transcript.py)

2. Clone this repository to your local machine using the following command

```shell
git clone https://github.com/AuracleTech/piai.git
```

3. Navigate to the project directory

```shell
cd piai
```

4. Install OpenAi Whisper

```shell
pip install -U openai-whisper
```

5. Install pipreqs to generates the dependencies

```shell
pip install pipreqs
```

6. Use pipreqs to generate the dependencies

```shell
pipreqs . --force
```

7. Install the required dependencies by running the following command

```shell
pip install -r requirements.txt
```

8. Optional : Create a .env file in the root directory and add the following variables

```shell
OPENAI_API_KEY=your-openai-api-key-here
```

9. Launch the app

```shell
python src/main.py
```

10. Speak with your new voice assistant
