"""
File represents configs of app flask
"""
import os
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    """
    Class to edit configs of app flask
    """
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=float(os.environ["JWT_ACCESS_TOKEN_EXPIRES"]))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=float(os.environ["JWT_REFRESH_TOKEN_EXPIRES"]))

    # development
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
