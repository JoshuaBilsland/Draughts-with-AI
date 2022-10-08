import mysql.connector

class Database:
    def __init__(self, host, username, password):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = None

        # Make connection and create cursor
        try:
            databaseConnection = mysql.connector.connect(host = self.__host, user = self.__username, password = self.__password)
            databaseCursor = databaseConnection.cursor()
        except Exception as error:
            print("********** ERROR **********")
            print(error)
            quit()

        # Create database if it doesn't exist + Set self.__database
        databaseCursor.execute("CREATE DATABASE IF NOT EXISTS DraughtsGame")
        self.__database = "DraughtsGame"

        # Connect to database
        databaseConnection = mysql.connector.connect(host = self.__host, user = self.__username, password = self.__password, database = self.__database)
        databaseCursor = databaseConnection.cursor()

        # Create tables if they don't exist
        databaseCursor.execute(""" CREATE TABLE IF NOT EXISTS UserStats (
            StatsID INT NOT NULL AUTO_INCREMENT,
            TotalNumberOfWinsAgainstAI INT UNSIGNED NOT NULL,
            TotalNumberOfDrawsAgainstAI INT UNSIGNED NOT NULL,
            TotalNumberOfLossesAgainstAI INT UNSIGNED NOT NULL,
            TotalNumberOfGamesPlayedAgainstAI INT UNSIGNED NOT NULL,
            HighestWinStreakAgainstAI INT UNSIGNED NOT NULL,
            CurrentWinStreakAgainstAI INT UNSIGNED NOT NULL,
            AverageNumberOfMovesToWinAgainstAI DECIMAL(6,3) NOT NULL,
            AverageNumberOfMovesToWinAgainstAICount INT UNSIGNED NOT NULL,
            AverageNumberOfMovesToWinAgainstAISum INT UNSIGNED NOT NULL,
            TotalNumberOfWinsAgainstPlayers INT UNSIGNED NOT NULL,
            TotalNumberOfDrawsAgainstPlayers INT UNSIGNED NOT NULL,
            TotalNumberOfLossesAgainstPlayers INT UNSIGNED NOT NULL,
            TotalNumberOfGamesPlayedAgainstPlayers INT UNSIGNED NOT NULL,
            HighestWinStreakAgainstPlayers INT UNSIGNED NOT NULL,
            CurrentWinStreakAgainstPlayers INT UNSIGNED NOT NULL,
            AverageNumberOfMovesToWinAgainstPlayers DECIMAL(6,3) NOT NULL,
            AverageNumberOfMovesToWinAgainstPlayersCount INT UNSIGNED NOT NULL,
            AverageNumberOfMovesToWinAgainstPlayersSum INT UNSIGNED NOT NULL,
            PRIMARY KEY (StatsID)
        )""")

        databaseCursor.execute("""CREATE TABLE IF NOT EXISTS UserAccount (
            AccountID INT NOT NULL AUTO_INCREMENT, 
            Username varchar(15) NOT NULL, 
            Password varchar(30) NOT NULL, 
            DataCreated DATE NOT NULL, 
            StatsID INT NOT NULL,
            PRIMARY KEY (AccountID),
            FOREIGN KEY (StatsID) REFERENCES UserStats(StatsID)
        )""")

        databaseConnection.close()
        databaseCursor.close()

    # Other
    def makeConnection(self):
        try:
            return mysql.connector.connect(host = self.__host, user = self.__username, password = self.__password, database = self.__database)
        except:
            return None

    def makeCursor(self, databaseConnection):
        try:
            return databaseConnection.cursor()
        except:
            return None


        