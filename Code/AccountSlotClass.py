class AccountSlot:
    
    def __init__(self):
        self.__username = None
        self.__database = None # database object (DatabaseClass.Database)
        self.__AccountID = None # ID of the record which stores the account in the database
        self.__colour = None # The colour the slot is playing as (in the game)
        self.__accountStats = { # Stores all the stats from the stats table in the database
            "Date Created":None,
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
        try:
            return self.__accountStats[statKey]
        except KeyError: # Return None if given key doesn't exist
            return None


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
    def signIn(self, username, password):
        checkUsernameAndPassword = self.__database.checkUsernameAndPassword(username, password) # Check if username & password match an account
        if not checkUsernameAndPassword: 
            return None # No account with that username and password was found 
        else: # Get the information for the account and update the slot to store it
            accountInformation = self.__database.getAccountInformation(username, password) # tuple of info 
            print(accountInformation)
            # Update slot information with account information
            self.setUsername(accountInformation[0][1])
            self.setAccountID(accountInformation[0][0])
            self.setAnAccountStat("Date Created", accountInformation[0][3])
            self.setAnAccountStat("Total Number of Wins Against AI", accountInformation[0][6])
            self.setAnAccountStat("Total Number of Draws Against AI", accountInformation[0][7])
            self.setAnAccountStat("Total Number of Losses Against AI", accountInformation[0][8])
            self.setAnAccountStat("Total Number of Games Played Against AI", accountInformation[0][9])
            self.setAnAccountStat("Highest Win Streak Against AI", accountInformation[0][10])
            self.setAnAccountStat("Current Win Streak Against AI", accountInformation[0][11])
            self.setAnAccountStat("Average Number of Moves to Win Against AI", accountInformation[0][12])
            self.setAnAccountStat("Average Number of Moves to Win Against AI Count", accountInformation[0][13])
            self.setAnAccountStat("Average Number of Moves to Win Against AI Sum", accountInformation[0][14])
            self.setAnAccountStat("Total Number of Wins Against Players", accountInformation[0][15])
            self.setAnAccountStat("Total Number of Draws Against Players", accountInformation[0][16])
            self.setAnAccountStat("Total Number of Losses Against Players", accountInformation[0][17])
            self.setAnAccountStat("Total Number of Games Played Against Players", accountInformation[0][18])
            self.setAnAccountStat("Highest Win Streak Against Players", accountInformation[0][19])
            self.setAnAccountStat("Current Win Streak Against Players", accountInformation[0][20])
            self.setAnAccountStat("Average Number of Moves to Win Against Players", accountInformation[0][21])
            self.setAnAccountStat("Average Number of Moves to Win Against Players Count", accountInformation[0][22])
            self.setAnAccountStat("Average Number of Moves to Win Against Players Sum", accountInformation[0][23])
            
            return False
            

    def signUp(self, username, password):
        self.__database.addNewUser(username, password)

    def signOut(self): # Clear the account slot information when the account is signed out, ready for next account to sign in
        self.__username = None
        self.__AccountID = None
        self.__colour = None
        self.__accountStats = dict.fromkeys(self.__accountStats, None)


        
    
