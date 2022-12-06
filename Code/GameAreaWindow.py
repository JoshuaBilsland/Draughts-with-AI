import pygame
import DisplayMessageWindow
import ChooseSlotWindow
import ChooseGameModeWindow
import ChooseGameOptionsWindow
import GameClass

def gameAreaWindow(window, slotOne, slotTwo):
    running = True

    while running:
        chosenGameMode = ChooseGameModeWindow.chooseGameMode(window, slotOne, slotTwo)
        if chosenGameMode != True: # if back button was not clicked - a game mode was chosen
            if chosenGameMode == "PvP":
                # PvP was chosen, check an account in signed in to each account - display error messages
                if slotOne.getAccountID() == None and slotTwo.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Either Slot")
                elif slotOne.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Slot One")
                elif slotTwo.getAccountID() == None:
                    backButtonClicked = DisplayMessageWindow.displayMessage(window, True, False, "No Account Signed in to Slot Two")
                # Slots do have an account signed in to them
                elif slotOne.getAccountID() != None and slotTwo.getAccountID() != None:
                    gameOptions = ChooseGameOptionsWindow.chooseGameOptions(window, chosenGameMode, slotOne, slotTwo)
                    if gameOptions != True: # not true means chosen options returned - True would mean that back button was clicked
                        runGame(window, slotOne, slotTwo, chosenGameMode, gameOptions)
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
                    else: # back button was clicked
                        running = True # go back to choose game mode window
        else: # back button was clicked
            running = False  
    return

def runGame(window, slotOne, slotTwo, chosenGameMode, gameOptions, chosenSlot="None"): # Carry out a game
    # Work out what to pass to the game class constructor
    if chosenGameMode == "PvP" and chosenSlot == "None": # If PvP chosen, no slot is chosen since both account slots are used
        game = GameClass.Game(window, chosenGameMode, gameOptions[0])
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
        if game.getGameFinished() == True:
            #---------------game.handleGameEnd()
            running = False
        else:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN: # Get where the user clicked and see what should happen (if anything)
                    mousePos = pygame.mouse.get_pos()
                    game.processClick(mousePos)
