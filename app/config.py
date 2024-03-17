"""
File represents configs of app flask
"""
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    """
    Class to edit configs of app flask
    """
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]

    # development
    SQLALCHEMY_TRACK_MODIFICATIONS = False
