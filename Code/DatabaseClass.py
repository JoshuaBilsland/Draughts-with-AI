import mysql.connector

class Database:
    __host = None
    __username = None
    __password = None

    def __init__(self, host, username, password):
        self.__host == host
        self.__username == username
        self.__password = password

        db = mysql.connector.connect(self.__host, self.__username, self.__password)
        dbCursor = db.cursor() # Executes SQL statements
        
        # Check if database exists. Create it if it doesn't
        dbCursor.execute("SHOW DATABASES")