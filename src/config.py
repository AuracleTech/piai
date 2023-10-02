import hashlib
import random


def generate_random_hash():
    random_data = str(random.getrandbits(256)).encode("utf-8")
    hash_value = hashlib.sha256(random_data).hexdigest()
    return hash_value


# Generate exit code
EXIT_CODE = generate_random_hash()

# Paths
RECORDINGS_PATH = "recordings"

# Whispering language
WHISPERING_LANGUAGE = "en"
