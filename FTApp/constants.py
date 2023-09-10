import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('SECRET_KEY')
