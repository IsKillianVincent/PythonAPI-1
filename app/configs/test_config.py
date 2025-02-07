import os
from dotenv import load_dotenv

load_dotenv()

TEST_VALID_API_KEY = os.getenv("TEST_VALID_API_KEY")
TEST_NOT_VALID_API_KEY = os.getenv("TEST_NOT_VALID_API_KEY")
