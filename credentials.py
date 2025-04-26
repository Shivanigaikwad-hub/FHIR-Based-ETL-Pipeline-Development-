import os

from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file if it exists
load_dotenv(find_dotenv())

BASE_SERVER_URL = os.getenv("BASE_SERVER_URL")
OPENEMR_API_URL = os.getenv("https://in-info-web20.luddy.indianapolis.iu.edu/interface/main/tabs/main.php?token_main=qzu0NCc8VlRrjDcqfBHaF8z4Jyd1Ny8VOOBOKaJn")