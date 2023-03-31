import pygame
import DisplayMessageWindow
import ChooseSlotWindow
import ChooseGameModeWindow
import ChooseGameOptionsWindow
import GameClass
from Constants import (
    COLOUR_ONE,
    COLOUR_TWO
)

def gameAreaWindow(window, slotOne, slotTwo):
    running = True

    while running:
        # Setup the game (get user to choose game mode and options)
        chosenGameMode = ChooseGameModeWindow.chooseGameMode(window, slotOne, slotTwo)
        if chosenGameMode != True: # if back button was not clicked - a game mode was chosen
            if chosenGameMode == "PvP":
                # PvP was chosen, check an account in signed in to each account - display error messages
                if slotOne.getAccountID() == None and slotTwo.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed into Either Slot")
                elif slotOne.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed into Slot One")
                elif slotTwo.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed into Slot Two")
                # Slots do have an account signed in to them
                elif slotOne.getAccountID() != None and slotTwo.getAccountID() != None:
                    gameOptions = ChooseGameOptionsWindow.chooseGameOptions(window, chosenGameMode, slotOne, slotTwo)
                    if gameOptions != True: # not true means chosen options returned - True would mean that back button was clicked
                        runGame(window, slotOne, slotTwo, chosenGameMode, gameOptions)
                        running = False
                    else: # back button was clicked
                        running = True # go back to choose game mode window

            else: # PvAI was chosen, check an account is signed into the chosen slot
                validChoice = False # True if non empty slot chosen or if back button is pressed (to get out of loop and return to previous window)
                while not validChoice:
                    chosenSlot = ChooseSlotWindow.chooseSlot(window, slotOne, slotTwo)
                    if chosenSlot == True: # Back button was clicked
                        validChoice = True # Get out of loop so can return to previous window
                    elif chosenSlot.getAccountID() == None: # slot is empty
                        backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Chosen Slot")
                    else: # slot has an account in it (not empty)
                        validChoice = True
                if chosenSlot != True: # slot chosen so continue (if it was true, back button was clicked so don't continue)
                    gameOptions = ChooseGameOptionsWindow.chooseGameOptions(window, chosenGameMode, slotOne, slotTwo)
                    if gameOptions != True:# not true means chosen options returned - True would mean that back button was clicked
                        runGame(window, slotOne, slotTwo, chosenGameMode, gameOptions, chosenSlot)
                        running = False
                    else: # back button was clicked
                        running = True # go back to choose game mode window
        else: # back button was clicked
            running = False  
    return


# Carry out a game
def runGame(window, slotOne, slotTwo, chosenGameMode, gameOptions, chosenSlot="None"): 
    # Work out what to pass to the game class constructor
    if chosenGameMode == "PvP" and chosenSlot == "None": # If PvP chosen, no slot is chosen since both account slots are used
        game = GameClass.Game(window, chosenGameMode, gameOptions[0], slotOne, slotTwo)
    else: # gameMode == "PvAI" and chosenSlot != "None" (In PvAI, one slot is chosen to be used)
        if chosenSlot == slotOne:
            game = GameClass.Game(window, chosenGameMode, gameOptions[0], slotOne, None, gameOptions[1])
        elif chosenSlot == slotTwo:
            game = GameClass.Game(window, chosenGameMode, gameOptions[0], None, slotTwo, gameOptions[1])

    # Game loop - used to carry out a game
    running = True
    while running:
        game.updateDisplay() # Keep refreshing screen/frame
        # Check if game needs to end
        if game.getGameFinished():
            winner = game.getWinner()
            slotOneTotalNumberOfMoves = game.getSlotOneTotalNumberOfMoves()
            slotTwoTotalNumberOfMoves = game.getSlotTwoTotalNumberOfMoves()

            # Update Account Stats and display winner
            if winner == None:
                message = "The Game Was a Draw"
                if chosenGameMode == "PvP":
                    # Increment number of draws against players by 1 (for both slots)
                    slotOneCurrentDrawsAgainstPlayers = slotOne.getAnAccountStat("Total Number of Draws Against Players")
                    slotTwoCurrentDrawsAgainstPlayers = slotTwo.getAnAccountStat("Total Number of Draws Against Players")
                    slotOne.setAnAccountStat("Total Number of Draws Against Players", (slotOneCurrentDrawsAgainstPlayers+1))
                    slotTwo.setAnAccountStat("Total Number of Draws Against Players", (slotTwoCurrentDrawsAgainstPlayers+1))
                    # End current win streak against players (for both slots)
                    slotOne.setAnAccountStat("Current Win Streak Against Players", 0)
                    slotTwo.setAnAccountStat("Current Win Streak Against Players", 0)
                if chosenGameMode == "PvAI":
                    if chosenSlot == slotOne:
                        # Increment number of draws against the AI by 1 (for slot one)
                        slotOneCurrentDrawsAgainstAI = slotOne.getAnAccountStat("Total Number of Draws Against AI")
                        slotOne.setAnAccountStat("Total Number of Draws Against AI", (slotOneCurrentDrawsAgainstAI+1))
                        # End current win streak against AI (for slot one)
                        slotOne.setAnAccountStat("Current Win Streak Against AI", 0)
                    else:
                        # Increment number of draws against the AI by 1 (for slot two)
                        slotTwoCurrentDrawsAgainstAI = slotTwo.getAnAccountStat("Total Number of Draws Against AI")
                        slotTwo.setAnAccountStat("Total Number of Draws Against AI", (slotTwoCurrentDrawsAgainstAI+1))
                        # End current win streak against AI (for slot two)
                        slotTwo.setAnAccountStat("Current Win Streak Against AI", 0)

            elif winner == "AI":
                message = "The AI Won the Game"
                if chosenSlot == slotOne:
                    # Increment number of losses against the AI by 1 (for slot one)
                    slotOneCurrentLossesAgainstAI = slotOne.getAnAccountStat("Total Number of Losses Against AI")
                    slotOne.setAnAccountStat("Total Number of Losses Against AI", (slotOneCurrentLossesAgainstAI+1))
                    # Increment number of games played against the AI by 1 (for slot one)
                    slotOneNumOfGamesPlayedAgainstAI = slotOne.getAnAccountStat("Total Number of Games Played Against AI")
                    slotOne.setAnAccountStat("Total Number of Games Played Against AI", (slotOneNumOfGamesPlayedAgainstAI+1))
                    # End current win streak against the AI (for slot one)
                    slotOne.setAnAccountStat("Current Win Streak Against AI", 0)
                else:
                    # Increment number of losses against the AI by 1 (for slot two)
                    slotTwoCurrentLossesAgainstAI = slotTwo.getAnAccountStat("Total Number of Losses Against AI")
                    slotTwo.setAnAccountStat("Total Number of Losses Against AI", (slotTwoCurrentLossesAgainstAI+1))
                    # Increment number of games played against the AI by 1 (for slot two)
                    slotOneNumOfGamesPlayedAgainstAI = slotOne.getAnAccountStat("Total Number of Games Played Against AI")
                    slotOne.setAnAccountStat("Total Number of Games Played Against AI", (slotOneNumOfGamesPlayedAgainstAI+1))
                    # End current win streak against the AI (for slot two)
                    slotTwo.setAnAccountStat("Current Win Streak Against AI", 0)

            else: # One of the slots won
                if winner == "S1": # slot one won
                    winningSlot = slotOne
                    if chosenGameMode == "PvP":
                        # Increment number of wins against players by 1 (for slot one)
                        slotOneCurrentWinsAgainstPlayers = slotOne.getAnAccountStat("Total Number of Wins Against Players")
                        slotOne.setAnAccountStat("Total Number of Wins Against Players", (slotOneCurrentWinsAgainstPlayers+1))
                        # Increment current win streak against players by 1 (for slot one)
                        slotOneCurrentWinStreakAgainstPlayers = slotOne.getAnAccountStat("Current Win Streak Against Players")
                        slotOne.setAnAccountStat("Current Win Streak Against Players", (slotOneCurrentWinStreakAgainstPlayers+1))
                        # Check if the current win streak against players is a new highest win streak (for slot one)
                        slotOneHighestWinStreakAgainstPlayers = slotOne.getAnAccountStat("Highest Win Streak Against Players")
                        slotOneCurrentWinStreakAgainstPlayers = slotOne.getAnAccountStat("Current Win Streak Against Players")  # Called again as it has been changed since the variable was last declared
                        if slotOneCurrentWinStreakAgainstPlayers > slotOneHighestWinStreakAgainstPlayers: 
                            slotOne.setAnAccountStat("Highest Win Streak Against Players", slotOneCurrentWinStreakAgainstPlayers)
                        # Update average number of moves to win against players, uses 'sum' and 'count' to get average (for slot one) 
                        slotOneTotalNumberOfMoves = game.getSlotOneTotalNumberOfMoves() # Get the number of moves slot one made in the game just played
                        slotOneExistingSum = slotOne.getAnAccountStat("Average Number of Moves to Win Against Players Sum") # Get the total number of moves the account in slot one has made in all their previously won games against other players 
                        slotOneNewSum = slotOneTotalNumberOfMoves + slotOneExistingSum # Get the new sum by adding them together
                        slotOne.setAnAccountStat("Average Number of Moves to Win Against Players Sum", slotOneNewSum)
                        
                        slotOneExistingCount = slotOne.getAnAccountStat("Average Number of Moves to Win Against Players Count") # Count is used to work out the average (how many games make up the moves sum)
                        slotOne.setAnAccountStat("Average Number of Moves to Win Against Players Count", (slotOneExistingCount+1))
                        
                        slotOneMovesSum = slotOne.getAnAccountStat("Average Number of Moves to Win Against Players Sum") # Call again as the values have been changed
                        slotOneMovesCount = slotOne.getAnAccountStat("Average Number of Moves to Win Against Players Count")
                        slotOneAverage = slotOneMovesSum / slotOneMovesCount
                        slotOne.setAnAccountStat("Average Number of Moves to Win Against Players", slotOneAverage)
                        # Increment number of losses against players by 1 (for slot two)
                        slotTwoCurrentLossesAgainstPlayers = slotTwo.getAnAccountStat("Total Number of Losses Against Players")
                        slotTwo.setAnAccountStat("Total Number of Losses Against Players",(slotTwoCurrentLossesAgainstPlayers+1))
                        # End current win streak against players (for slot two)
                        slotTwo.setAnAccountStat("Current Win Streak Against Players", 0)
                        # Increment number of games played against players by 1 (for both slots)
                        slotOneNumOfGamesPlayedAgainstPlayers = slotOne.getAnAccountStat("Total Number of Games Played Against Players")
                        slotOne.setAnAccountStat("Total Number of Games Played Against Players", (slotOneNumOfGamesPlayedAgainstPlayers+1))
                        slotTwoNumOfGamesPlayedAgainstPlayers = slotTwo.getAnAccountStat("Total Number of Games Played Against Players")
                        slotTwo.setAnAccountStat("Total Number of Games Played Against Players", (slotTwoNumOfGamesPlayedAgainstPlayers+1))
                    else:
                        # Increment number of wins against the AI by 1 (for slot one)
                        slotOneCurrentWinsAgainstAI = slotOne.getAnAccountStat("Total Number of Wins Against AI")
                        slotOne.setAnAccountStat("Total Number of Wins Against AI", (slotOneCurrentWinsAgainstAI+1))
                        # Increment current win streak against the AI by 1 (for slot one)
                        slotOneCurrentWinStreakAgainstAI = slotOne.getAnAccountStat("Current Win Streak Against AI")
                        slotOne.setAnAccountStat("Current Win Streak Against AI", (slotOneCurrentWinStreakAgainstAI+1))
                        # Check if the current win streak against the AI is a new highest win streak (for slot one)
                        slotOneCurrentWinStreakAgainstAI = slotOne.getAnAccountStat("Current Win Streak Against AI")
                        slotOneHighestWinStreakAgainstAI = slotOne.getAnAccountStat("Highest Win Streak Against AI")
                        if slotOneCurrentWinStreakAgainstAI > slotOneHighestWinStreakAgainstAI:
                            slotOne.setAnAccountStat("Highest Win Streak Against AI", slotOneCurrentWinStreakAgainstAI)
                        # Update average number of moves to win against AI, uses 'sum' and 'count' to get average (for slot one) 
                        slotOneTotalNumberOfMoves = game.getSlotOneTotalNumberOfMoves() # Get the number of moves slot one made in the game just played
                        slotOneExistingSum = slotOne.getAnAccountStat("Average Number of Moves to Win Against AI Sum") # Get the total number of moves the account in slot one has made in all their previously won games against the AI   
                        slotOneNewSum = slotOneTotalNumberOfMoves + slotOneExistingSum # Get the new sum by adding them together
                        slotOne.setAnAccountStat("Average Number of Moves to Win Against AI Sum", slotOneNewSum)

                        slotOneExistingCount = slotOne.getAnAccountStat("Average Number of Moves to Win Against AI Count") # Count is used to work out the average (how many games make up the moves sum)
                        slotOne.setAnAccountStat("Average Number of Moves to Win Against AI Count", (slotOneExistingCount+1))
                        
                        slotOneMovesSum = slotOne.getAnAccountStat("Average Number of Moves to Win Against AI Sum") # Call again as the values have been changed
                        slotOneMovesCount = slotOne.getAnAccountStat("Average Number of Moves to Win Against AI Count")
                        slotOneNewAverage = slotOneMovesSum / slotOneMovesCount
                        slotOne.setAnAccountStat("Average Number of Moves to Win Against AI", slotOneNewAverage)
                        # Increment number of games played against the AI by 1 (for slot one)
                        slotOneNumOfGamesPlayedAgainstAI = slotOne.getAnAccountStat("Total Number of Games Played Against AI")
                        slotOne.setAnAccountStat("Total Number of Games Played Against AI", (slotOneNumOfGamesPlayedAgainstAI+1))

                else: # slot two won
                    winningSlot = slotTwo
                    if chosenGameMode == "PvP":
                        # Increment number of wins against players by 1 (for slot two)
                        slotTwoCurrentWinsAgainstPlayers = slotTwo.getAnAccountStat("Total Number of Wins Against Players")
                        slotTwo.setAnAccountStat("Total Number of Wins Against Players", (slotTwoCurrentWinsAgainstPlayers+1))
                        # Increment current win streak against players by 1 (for slot two)
                        slotTwoCurrentWinStreakAgainstPlayers = slotTwo.getAnAccountStat("Current Win Streak Against Players")
                        slotTwo.setAnAccountStat("Current Win Streak Against Players", (slotTwoCurrentWinStreakAgainstPlayers+1))
                        # Check if the current win streak against players is a new highest win streak (for slot two)
                        slotTwoHighestWinStreakAgainstPlayers = slotOne.getAnAccountStat("Highest Win Streak Against Players")
                        slotTwoCurrentWinStreakAgainstPlayers = slotTwo.getAnAccountStat("Current Win Streak Against Players") # Called again as it has been changed since the variable was last declared
                        if slotTwoCurrentWinStreakAgainstPlayers > slotTwoHighestWinStreakAgainstPlayers:
                            slotTwo.setAnAccountStat("Highest Win Streak Against Players", slotTwoCurrentWinStreakAgainstPlayers)
                        # Update average number of moves to win against players, uses 'sum' and 'count' to get average (for slot two) 
                        slotTwoTotalNumberOfMoves = game.getSlotTwoTotalNumberOfMoves() # Get the number of moves slot two made in the game just played
                        slotTwoExistingSum = slotTwo.getAnAccountStat("Average Number of Moves to Win Against Players Sum") # Get the total number of moves the account in slot two has made in all their previously won games against other players 
                        slotTwoNewSum = slotTwoTotalNumberOfMoves + slotTwoExistingSum # Get the new sum by adding them together
                        slotTwo.setAnAccountStat("Average Number of Moves to Win Against Players Sum", slotTwoNewSum)

                        slotTwoExistingCount = slotTwo.getAnAccountStat("Average Number of Moves to Win Against Players Count") # Count is used to work out the average (how many games make up the moves sum)
                        slotTwo.setAnAccountStat("Average Number of Moves to Win Against Players Count", (slotTwoExistingCount+1))
                        
                        slotTwoMovesSum = slotTwo.getAnAccountStat("Average Number of Moves to Win Against Players Sum") # Call again as the values have been changed
                        slotTwoMovesCount = slotTwo.getAnAccountStat("Average Number of Moves to Win Against Players Count")
                        slotTwoAverage = slotTwoMovesSum / slotTwoMovesCount
                        slotTwo.setAnAccountStat("Average Number of Moves to Win Against Players", slotTwoNewAverage)
                        # Increment number of losses against players by 1 (for slot one)
                        slotOneCurrentLossesAgainstPlayers = slotOne.getAnAccountStat("Total Number of Losses Against Players")
                        slotOne.setAnAccountStat("Total Number of Losses Against Players", (slotOneCurrentLossesAgainstPlayers+1))
                        # End current win streak against players (for slot two)
                        slotOne.setAnAccountStat("Current Win Streak Against Players", 0)
                        # Increment number of games played against players by 1 (for both slots)
                        slotOneNumOfGamesPlayedAgainstPlayers = slotOne.getAnAccountStat("Total Number of Games Played Against Players")
                        slotOne.setAnAccountStat("Total Number of Games Played Against Players", (slotOneNumOfGamesPlayedAgainstPlayers+1))
                        slotTwoNumOfGamesPlayedAgainstPlayers = slotTwo.getAnAccountStat("Total Number of Games Played Against Players")
                        slotTwo.setAnAccountStat("Total Number of Games Played Against Players", (slotTwoNumOfGamesPlayedAgainstPlayers+1))
                    else:
                        # Increment number of wins against the AI by 1 (for slot two)
                        slotTwoCurrentWinsAgainstAI = slotTwo.getAnAccountStat("Total Number of Wins Against AI")
                        slotTwo.setAnAccountStat("Total Number of Wins Against AI", (slotTwoCurrentWinsAgainstAI+1))
                        # Increment current win streak against the AI by 1 (for slot two)
                        slotTwoCurrentWinStreakAgainstAI = slotTwo.getAnAccountStat("Current Win Streak Against AI")
                        slotTwo.setAnAccountStat("Current Win Streak Against AI", (slotTwoCurrentWinStreakAgainstAI+1))
                        # Check if the current win streak against the AI is a new highest win streak (for slot two)
                        slotTwoCurrentWinStreakAgainstAI = slotTwo.getAnAccountStat("Current Win Streak Against AI")
                        slotTwoHighestWinStreakAgainstAI = slotTwo.getAnAccountStat("Highest Win Streak Against AI")
                        if slotTwoCurrentWinStreakAgainstAI > slotTwoHighestWinStreakAgainstAI:
                            slotTwo.setAnAccountStat("Highest Win Streak Against AI", slotTwoCurrentWinStreakAgainstAI)
                        # Update average number of moves to win against AI, uses 'sum' and 'count' to get average (for slot two) 
                        slotTwoTotalNumberOfMoves = game.getSlotTwoTotalNumberOfMoves() # Get the number of moves slot two made in the game just played
                        slotTwoExistingSum = slotTwo.getAnAccountStat("Average Number of Moves to Win Against AI Sum") # Get the total number of moves the account in slot two has made in all their previously won games against the AI   
                        slotTwoNewSum = slotTwoTotalNumberOfMoves + slotTwoExistingSum # Get the new sum by adding them together
                        slotTwo.setAnAccountStat("Average Number of Moves to Win Against AI Sum", slotTwoNewSum)

                        slotTwoExistingCount = slotTwo.getAnAccountStat("Average Number of Moves to Win Against AI Count") # Count is used to work out the average (how many games make up the moves sum)
                        slotTwo.setAnAccountStat("Average Number of Moves to Win Against AI Count", (slotTwoExistingCount+1))
                        
                        slotTwoMovesSum = slotTwo.getAnAccountStat("Average Number of Moves to Win Against AI Sum") # Call again as the values have been changed
                        slotTwoMovesCount = slotTwo.getAnAccountStat("Average Number of Moves to Win Against AI Count")
                        slotTwoNewAverage = slotTwoMovesSum / slotTwoMovesCount
                        slotTwo.setAnAccountStat("Average Number of Moves to Win Against AI", slotTwoNewAverage)
                        # Increment number of games played against the AI by 1 (for slot two)
                        slotTwoNumOfGamesPlayedAgainstAI = slotTwo.getAnAccountStat("Total Number of Games Played Against AI")
                        slotTwo.setAnAccountStat("Total Number of Games Played Against AI", (slotTwoNumOfGamesPlayedAgainstAI+1))

                # Generate the message to display on the end of game window (to show who won)
                username = winningSlot.getUsername() # Get the username of the account in the winning slot
                message = str(username) + " Won the Game"

            # Use the now updated dictionary in the account slot/s to update the database (to reflect the changes there as well)
            if chosenGameMode == "PvP":
                slotOne.applyDictionaryChangesToDatabase()
                slotTwo.applyDictionaryChangesToDatabase()
            else:
                if chosenSlot == slotOne:
                    slotOne.applyDictionaryChangesToDatabase()
                else:
                    slotTwo.applyDictionaryChangesToDatabase()
                
            # Display the message
            DisplayMessageWindow.displayMessage(window, False, True, message) # Used to display game results
            running = False
        else:
            # Check if AI move needs to be carried out
            if game.getTurn()[0] == "AI":
                game.AIMove()
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN: # Get where the user clicked and see what should happen (if anything)
                    mousePos = pygame.mouse.get_pos()
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    game.processClick(mousePos)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)