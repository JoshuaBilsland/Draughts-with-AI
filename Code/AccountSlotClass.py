class AccountSlot:
    
    def __init__(self):
        self.__username = None
        self.__database = None # database object (DatabaseClass.Database)
        self.__AccountID = None # ID of the record which stores the account in the database
        self.__colour = None # The colour the slot is playing as (in the game)
        self.__accountStats = { # Stores all the stats from the stats table in the database
            "Total Number of Wins Against AI":None,
            "Total Number of Draws Against AI":None,
            "Total Number of Losses Against AI":None,
            "Total Number of Games Played Against AI":None,
            "Highest Win Streak Against AI":None,
            "Current Win Streak Against AI":None,
            "Average Number of Moves to Win Against AI":None,
            "Average Number of Moves to Win Against AI Count":None,
            "Average Number of Moves to Win Against AI Sum":None,
            "Total Number of Wins Against Players":None,
            "Total Number of Draws Against Players":None,
            "Total Number of Losses Against Players":None,
            "Total Number of Games Played Against Players":None,
            "Highest Win Streak Against Players":None,
            "Current Win Streak Against Players":None,
            "Average Number of Moves to Win Against Players":None,
            "Average Number of Moves to Win Against Players Count":None,
            "Average Number of Moves to Win Against Players Sum":None
        } 


    # Get
    def getUsername(self):
        return self.__username

    def getDatabase(self):
        return self.__database

    def getAccountID(self):
        return self.__AccountID

    def getColour(self):
        return self.__colour
    
    def getAllAccountStats(self): # Return all the stats in the dictionary
        return self.__accountStats

    def getAnAccountStat(self, statKey): # Return a specific stat from the dictionary
        return self.__accountStats
    

    # Set
    def setUsername(self, username):
        self.__username = username

    def setDatabase(self, databaseObject):
        self.__database = databaseObject

    def setAccountID(self, ID):
        self.__AccountID = ID

    def setColour(self, colour):
        self.__colour = colour

    def setAccountStats(self, accountStatsDictionary): # Update with a new dictionary
        self.__accountStats = accountStatsDictionary

    def setAnAccountStat(self, key, value): # Update a specific stat
        if key in self.__accountStats: # Check that the stat exists, stops new ones being added
            self.__accountStats[key] = value
    

    # Other
    def signOut(self): # Clear the account slot information when the account is signed out, ready for next account to sign in
        self.__username = None
        self.__AccountID = None
        self.__colour = None
        self.__accountStats = dict.fromkeys(self.__accountStats, None)

    def signUp(self, username, password):
        self.__database.addNewUser(username, password)
        
    
