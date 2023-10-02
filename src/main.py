import transcriber
import interpreter
import threading
import recorder
import config
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import Queue

# Start the browser
driver = webdriver.Chrome()
driver.get("https://pi.ai/talk")
textarea = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located(
        (
            By.CSS_SELECTOR,
            "textarea.block.w-full.resize-none.overflow-y-hidden.whitespace-pre-wrap.bg-transparent.outline-none.placeholder\\:text-brand-gray-400.font-serif.font-normal.text-body-chat-m.lg\\:text-body-chat-l",
        )
    )
)

# Create queues
recordings_queue = Queue()
transcript_queue = Queue()

# Start the threads
thread_transcribe = threading.Thread(
    target=transcriber.transcribe, args=(recordings_queue, transcript_queue)
)
thread_interpret = threading.Thread(
    target=interpreter.interpret, args=(transcript_queue, textarea)
)


def clear_queue(queue):
    while not queue.empty():
        queue.get()


try:
    print("Create recordings directory...")
    if not os.path.exists(config.RECORDINGS_PATH):
        os.makedirs(config.RECORDINGS_PATH)

    print("Waiting 4s page loading...")
    time.sleep(4)

    print("Starting threads...")
    thread_interpret.start()
    thread_transcribe.start()
    recorder.listen(config.RECORDINGS_PATH, recordings_queue)

except KeyboardInterrupt:
    print("Stopping...")

    print("Stopping browser...")
    driver.quit()

    print("Clearing queues...")
    clear_queue(recordings_queue)
    clear_queue(transcript_queue)

    print("Send exit code to all queues...")
    recordings_queue.put(config.EXIT_CODE)
    transcript_queue.put(config.EXIT_CODE)

    print("Waiting for threads to finish...")
    thread_transcribe.join()
    thread_interpret.join()

    print("Deleting recordings directory...")
    for filename in os.listdir(config.RECORDINGS_PATH):
        os.remove(os.path.join(config.RECORDINGS_PATH, filename))
    os.rmdir(config.RECORDINGS_PATH)

    print("Program terminated")
    exit(0)
