"""Handle various database operations"""

import os
import sqlite3
import checkin.common as common
import pandas as pd

from checkin.errors import *


# ---------------------------- Private parameters ---------------------------- #
_SQL_DB_NAME = "users.db"
_USERS_TABLE_NAME = "users"
_SQL_DB_FULL_PATH = os.path.join(common.SITE_DATA_DIR, _SQL_DB_NAME)

def init():

    if not os.path.exists(_SQL_DB_FULL_PATH):
        new_users_db()

class User:

    # def __init__(self, user_name: str, user_email: str, password_hashed, last_login):
    def __init__(self, user_name: str, password_hashed, last_login):

        self.user_name = user_name
        # self.user_email = user_email
        self.password_hashed = password_hashed
        self.last_login = last_login

    def __str__(self) -> str:
        return f"{self.user_name}"

    def __repr__(self) -> str:
        return f"{self.user_name}"


    def sql_insert(self) -> str:
        """Return the SQL query to insert this user into the database"""

        return f"""
        INSERT INTO {_USERS_TABLE_NAME}
        VALUES ('{self.user_name}', '{self.password_hashed}', {self.last_login})
        """

    def to_row(self) -> pd.Series:

        return pd.Series({
            "user_name": self.user_name,
            "password_hashed": self.password_hashed,
            "last_login": self.last_login
        })

    @staticmethod
    def from_row(row: pd.Series):

        return User(row["user_name"], row["password_hashed"], row["last_login"])




def users_db_path() -> str:
    return _SQL_DB_FULL_PATH

def connect_to_users() -> sqlite3.Connection:
    return sqlite3.connect(users_db_path())

def new_users_db():
    # We want to create a new db file with the fillowing schema
    # CREATE TABLE(user_name TEXT, user_email TEXT, password_hashed TEXT, last_login INTEGER)
    # - last_login is the unix time of the last login
    db = users_db_path()

    if os.path.exists(db):
        os.remove(db)

    try:
        con = sqlite3.connect(db)

        # con.execute("CREATE TABLE users (user_name TEXT, user_email TEXT, password_hashed TEXT, last_login INTEGER)")
        con.execute("CREATE TABLE users (user_name TEXT, password_hashed TEXT, last_login INTEGER)")


        con.close()
    except:
        common.log_content(f"Exception occured when trying to connect to sqlite3 db: '{db}'")

def add_user(user: User):

    # Add a user to the data_base

    # Open up a connection to the user database, and add this user
    # if the user doesnt already exist.

    users = get_users_df()

    # Check if the user is currently in the database


    # Check if there are any conflicts
    # if the user does not already exist

    # If the username is already taken, we cannot add the user

    if any(users["user_name"] == user.user_name):

        raise UserNameTakenError(f"Username: {user.user_name} already in use")

    # if any(users["user_email"] == user.user_email):

    #     raise EmailTakenError(f"Email: {user.user_email} already associated with an account")

    con = connect_to_users()
    con.execute(user.sql_insert())
    con.commit()
    con.close()


def get_users_df() -> pd.DataFrame:
    query = f"""SELECT * from {_USERS_TABLE_NAME}"""

    con = connect_to_users()
    df = pd.read_sql_query(query, con)
    con.close()

    return df

def get_users() -> list[User]:

    return [User.from_row(r) for (_, r) in get_users_df().iterrows()]

