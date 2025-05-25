from dotenv import load_dotenv, find_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

SQL_DATABASE = env.get('SQL_DATABASE')
SQL_USER = env.get('SQL_USER')
SQL_PASSWORD = env.get('SQL_PASSWORD')
SQL_HOST = env.get('SQL_HOST')
SQL_PORT = env.get('SQL_PORT')

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/pythonProject")

