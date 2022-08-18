import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
