from dotenv import load_dotenv
import openai
import os
import config
from selenium.webdriver.common.keys import Keys


def interpret(transcript_queue, textarea):
    print("Interpreting...")

    # Load environment variables from .env
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # MAX_TOKENS = 32

    while True:
        # Get the transcript from the queue
        transcript = transcript_queue.get()

        # If we receive exit code, stop
        if transcript == config.EXIT_CODE:
            break

        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "Reply Y if an AI should reply to this, otherwise N",
        #         },
        #         {"role": "user", "content": transcript},
        #     ],
        #     max_tokens=MAX_TOKENS,
        # )

        # # Trim and clean the message choice
        # is_question = completion.choices[0].message.content.strip()

        # print(f'IS_QUESTION: "{is_question}"')

        # If it is a question, ask pi ai
        # if is_question == "Y" or is_question == "y":
        textarea.clear()
        textarea.send_keys(transcript)
        textarea.send_keys(Keys.RETURN)

    print("Stopped interpreting")
