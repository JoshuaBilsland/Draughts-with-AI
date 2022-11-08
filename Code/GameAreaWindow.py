import pygame
import DisplayMessageWindow
import ChooseSlotWindow
import ChooseGameModeWindow
import ChooseGameOptionsWindow

def gameAreaWindow(window,slotOne, slotTwo):
    running = True

    while running:
        chosenMode = ChooseGameModeWindow.chooseGameMode(window, slotOne, slotTwo)
        if chosenMode != True: # if back button was not clicked - a game mode was chosen
            if chosenMode == "PvP":
                # PvP was chosen, check an account in signed in to each account - display error messages
                if slotOne.getAccountID() == None and slotTwo.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Either Slot")
                elif slotOne.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Slot One")
                elif slotOne.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Slot Two")
                # Slots do have an account signed in to them
                elif slotOne.getAccountID() != None and slotTwo.getAccountID() != None:
                    gameOptions = ChooseGameOptionsWindow.chooseGameOptions(window, chosenMode, slotOne, slotTwo)
                    if gameOptions != True:
                        print("READY TO SETUP GAME")
                    else: # back button was clicked
                        running = True

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
                    gameOptions = ChooseGameOptionsWindow.chooseGameOptions(window, chosenMode, slotOne, slotTwo)
                    if gameOptions != True: # continue button clicked (options chosen)
                        print("READY TO SETUP GAME")
                    else: # back button was clicked
                        running = True # go back to choose game mode window
        else: # back button was clicked
            running = False  
    return