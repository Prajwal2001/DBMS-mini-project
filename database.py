import hashlib
import mysql.connector
import yaml


class Database:
    def __init__(self):
        with open('./credentials.yaml') as f:
            self.__data = yaml.load(f, Loader=yaml.FullLoader)
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user=self.__data["user"],
            password=self.__data["password"],
            database=self.__data["database"],
            autocommit=True
        )

        self.__cursor = self.__mydb.cursor()

    def add_user(self, user: list):
        """Adds a user to the database, by accepting a list consisting of username, password and email.
        And returns the updated table values in a list of key value pairs"""
        u_name, email, password = user

        try:
            self.__cursor.execute(
                f"insert into users values(null, '{u_name}', '{hashlib.md5(password.encode()).hexdigest()}', '{email}')")
        except mysql.connector.errors.IntegrityError:
            return None

        self.__cursor.execute(f"select * from users")

        return [{
            "user_id": item[0],
            "user_name": item[1],
            "email": item[2],
            "password": item[3]
        } for item in self.__cursor.fetchall()]

    def does_user_exist(self, user: list):
        self.__cursor.execute(
            f"select * from users where u_name = '{user[0]}' and password = '{hashlib.md5(user[1].encode()).hexdigest()}'")
        return bool(self.__cursor.fetchall())
