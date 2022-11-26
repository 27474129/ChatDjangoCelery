import os
from dotenv import load_dotenv


load_dotenv()


DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_HOST = os.getenv("DB_HOST")
SECRET_KEY = os.getenv("SECRET_KEY")

