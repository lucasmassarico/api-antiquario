# user.py

"""
Module containing the definition of the UserModel class to represent users in the database.
"""

from app import db


class UserModel(db.Model):
    """
    Class that represents a user in the application.

    Attributes:
        id (int): Primary key, unique identifier of the user.
        name (str): Name of the user.
        email (str): User's email address, must be unique.
        password (str): Encrypted password of the user.
        active (bool): Indicates whether the user's account is active.
        access_role (int): Access level of the user, default is 1.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    access_role = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: The name of the user.
        """
        return f"{self.name}"
