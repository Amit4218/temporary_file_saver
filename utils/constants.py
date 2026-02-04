import os

from dotenv import load_dotenv

load_dotenv()


TEMP_FOLDER = "temp"

MAX_FILE_SIZE = 30 * 1024 * 1024

HOST_URL = os.getenv("HOST_URL")

DATABASE_URL = os.getenv("DATABASE_URL")
