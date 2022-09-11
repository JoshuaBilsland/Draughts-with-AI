class AccountSlot():
    
    def __init__(self):
        self.__username = None
        self.__userDatabaseID = None # Get the ID of the record which stores the account 
        self.__colour = None # The colour the slot is playing as (in the game)
        self.__accountStats = {} # Stores all the stats from the stats table in the database

    def clear(self): # Clear the account slot information when the account is signed out, ready for next account to sign in
        self.__username = None
        self.__userDatabaseID = None
        self.__colour = None
        self.__accountStats = {}

    # Get
    def getUsername(self):
        return self.__username

    def getUserDatabaseID(self):
        return self.__userDatabaseID

    def getColour(self):
        return self.__colour
    
    def getAllAccountStats(self): # Return all the stats in the dictionary
        return self.__accountStats

    def getAnAccountStat(self, statKey): # Return a specific stat from the dictionary
        return self.__accountStats
    
    # Set - For updating information
    def setUsername(self, username):
        self.__username = username

    def setUserDatabaseID(self, ID):
        self.__userDatabaseID = ID

    def setColour(self, colour):
        self.__colour = colour

    def setAccountStats(self, accountStatsDictionary): # Update with a new dictionary
        self.__accountStats = accountStatsDictionary

    def setAnAccountStat(self, key, value): # Update a specific stat
        if key in self.__accountStats: # Check that the stat exists, stops new ones being added
            self.__accountStats[key] = value
    
    

    
