from base64 import encode
import mysql.connector
import hashlib

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


        # Reconnect to database
        databaseCursor.close()
        databaseConnection.close()
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
            PRIMARY KEY (StatsID))
        """)

        databaseCursor.execute("""CREATE TABLE IF NOT EXISTS UserAccount (
            AccountID INT NOT NULL AUTO_INCREMENT, 
            Username varchar(255) NOT NULL, 
            Password varchar(255) NOT NULL, 
            DateCreated DATE NOT NULL, 
            StatsID INT NOT NULL,
            PRIMARY KEY (AccountID),
            FOREIGN KEY (StatsID) REFERENCES UserStats(StatsID))
        """)


        databaseCursor.close()
        databaseConnection.close()


    # Other
    def makeConnection(self): 
        return mysql.connector.connect(host = self.__host, user = self.__username, password = self.__password, database = self.__database)


    def makeCursor(self, databaseConnection):
        return databaseConnection.cursor()


    def checkUsernameAndPassword(self, username, password):
        databaseConnection = self.makeConnection()
        databaseCursor = self.makeCursor(databaseConnection)

        encodedPassword = password.encode() # Encode with UTF-8
        hashedPassword = hashlib.sha256(encodedPassword) # Hash password
        
        preparedQuery = "SELECT AccountID FROM UserAccount WHERE Username=%s AND Password=%s"
        databaseCursor.execute(preparedQuery, (username, hashedPassword.hexdigest()))

        if databaseCursor.fetchall() == []:
            boolean = False
        else:
            boolean = True

        databaseCursor.close()
        databaseConnection.close()

        return boolean


    def getAccountInformation(self, username, password):
        databaseConnection = self.makeConnection()
        databaseCursor = self.makeCursor(databaseConnection)

        encodedPassword = password.encode() # Encode with UTF-8
        hashedPassword = hashlib.sha256(encodedPassword) # Hash password

        preparedQuery = "SELECT * FROM UserAccount, UserStats WHERE Username=%s AND Password=%s AND UserAccount.StatsID = UserStats.StatsID"
        # Return account information
        accountInformation = databaseCursor.execute(preparedQuery, (username, hashedPassword.hexdigest()))
        
        return databaseCursor.fetchall()
        

    def isUsernameUnique(self, username):
        databaseConnection = self.makeConnection()
        databaseCursor = self.makeCursor(databaseConnection)

        preparedQuery = "SELECT * FROM UserAccount WHERE Username=%s"
        usernameForPlaceholder = (username,) # Tuple needed for preparedQuery
        databaseCursor.execute(preparedQuery,usernameForPlaceholder)
        
        if databaseCursor.fetchall() == []:
            boolean = True
        else:
            boolean = False

        databaseCursor.close()
        databaseConnection.close()
        
        return boolean


    def addNewUser(self, username, password): # Add a new user to the database
        databaseConnection = self.makeConnection()
        databaseCursor =  self.makeCursor(databaseConnection)

        encodedPassword = password.encode() # Encode with UTF-8
        hashedPassword = hashlib.sha256(encodedPassword) # Hash password before storing in database
 
        if self.isUsernameUnique(username):
            databaseCursor.execute(""" INSERT INTO UserStats (
                TotalNumberOfWinsAgainstAI,
                TotalNumberOfDrawsAgainstAI,
                TotalNumberOfLossesAgainstAI,
                TotalNumberOfGamesPlayedAgainstAI,
                HighestWinStreakAgainstAI,
                CurrentWinStreakAgainstAI,
                AverageNumberOfMovesToWinAgainstAI,
                AverageNumberOfMovesToWinAgainstAICount,
                AverageNumberOfMovesToWinAgainstAISum,
                TotalNumberOfWinsAgainstPlayers,
                TotalNumberOfDrawsAgainstPlayers,
                TotalNumberOfLossesAgainstPlayers,
                TotalNumberOfGamesPlayedAgainstPlayers,
                HighestWinStreakAgainstPlayers,
                CurrentWinStreakAgainstPlayers,
                AverageNumberOfMovesToWinAgainstPlayers,
                AverageNumberOfMovesToWinAgainstPlayersCount,
                AverageNumberOfMovesToWinAgainstPlayersSum) 
                VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
            """)
            databaseConnection.commit()

            preparedQuery = "INSERT INTO UserAccount (Username, Password, DateCreated, StatsID) VALUES(%s,%s,NOW(),LAST_INSERT_ID())"
            databaseCursor.execute(preparedQuery, (username, hashedPassword.hexdigest()))
            databaseConnection.commit()

            databaseCursor.close()
            databaseConnection.close()

    
    def updateDatabaseWithDictionary(self, dictionary, StatsID):
        databaseConnection = self.makeConnection()
        databaseCursor = self.makeCursor(databaseConnection)

        valuesForStatement = list(dictionary.values())[1:] # List slicing is used to ignore the first key (and value) as this is the date the account was created which is not in the UserStats table (and does not even change)

        valuesForStatement.append(StatsID) # Add the value of StatsID to end so it can be put in the placeholder for the WHERE part

        preparedQuery = """ UPDATE UserStats SET                 
                TotalNumberOfWinsAgainstAI = %s,
                TotalNumberOfDrawsAgainstAI = %s,
                TotalNumberOfLossesAgainstAI = %s,
                TotalNumberOfGamesPlayedAgainstAI = %s,
                HighestWinStreakAgainstAI = %s,
                CurrentWinStreakAgainstAI = %s,
                AverageNumberOfMovesToWinAgainstAI = %s,
                AverageNumberOfMovesToWinAgainstAICount = %s,
                AverageNumberOfMovesToWinAgainstAISum = %s,
                TotalNumberOfWinsAgainstPlayers = %s,
                TotalNumberOfDrawsAgainstPlayers = %s,
                TotalNumberOfLossesAgainstPlayers = %s,
                TotalNumberOfGamesPlayedAgainstPlayers = %s,
                HighestWinStreakAgainstPlayers = %s,
                CurrentWinStreakAgainstPlayers = %s,
                AverageNumberOfMovesToWinAgainstPlayers = %s,
                AverageNumberOfMovesToWinAgainstPlayersCount = %s,
                AverageNumberOfMovesToWinAgainstPlayersSum = %s
                WHERE StatsID = %s
        """
        print("valuesForStatement", valuesForStatement)
        databaseCursor.execute(preparedQuery, valuesForStatement)
        databaseConnection.commit()

        databaseCursor.close()
        databaseConnection.close()


