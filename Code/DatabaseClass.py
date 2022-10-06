import mysql

class Database:
    def __init__(self, host, username, password):
        self.__host = host
        self.__username = username
        self.__password = password

        databaseConnection = mysql.connector.connect(self.__host, self.__username, self.__password)
        databaseCursor = databaseConnection.cursor() # Executes SQL statements
        
