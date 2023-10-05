import transcriber
import interpreter
import threading
import recorder
import config
import os
import time
from queue import Queue


# Create queues
recordings_queue = Queue()
transcript_queue = Queue()

# Start the threads
thread_transcribe = threading.Thread(
    target=transcriber.transcribe, args=(recordings_queue, transcript_queue)
)
thread_interpret = threading.Thread(
    target=interpreter.interpret, args=(transcript_queue,)
)


def clear_queue(queue):
    while not queue.empty():
        queue.get()


try:
    print("Create recordings directory...")
    if not os.path.exists(config.RECORDINGS_PATH):
        os.makedirs(config.RECORDINGS_PATH)

    print("Starting threads...")
    thread_interpret.start()
    thread_transcribe.start()
    recorder.listen(config.RECORDINGS_PATH, recordings_queue)

except KeyboardInterrupt:
    print("Stopping...")

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
