from re import L
from xml.etree.ElementTree import TreeBuilder
import pygame
import ButtonClass
import ChooseSlotWindow
import GetUsernameAndPasswordWindow
import DisplayMessageWindow
from Constants import (
    WIDTH, 
    HEIGHT, 
    REGULAR_BUTTON_WIDTH, 
    REGULAR_BUTTON_HEIGHT,
    REGULAR_BUTTON_X,
    REGULAR_BUTTON_Y,
    BACK_BUTTON_WIDTH,
    BACK_BUTTON_HEIGHT,
    BACK_BUTTON_X,
    BACK_BUTTON_Y, 
    BEIGE, 
    MENU_BACKGROUND_IMAGE
)

# Displays the different options related to the accounts (Sign in, sign out, etc) - Displays once the user has clicked the account button on the main menu
def accountAreaWindow(window, slotOne, slotTwo):
    running = True

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        signInButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y, REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Sign In")
        signInButton.draw(window)

        signUpButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+(HEIGHT*0.2), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Sign Up")
        signUpButton.draw(window)

        signOutButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+(HEIGHT*0.4), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Sign Out")
        signOutButton.draw(window)

        viewAccountButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+(HEIGHT*0.6), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "View Account")
        viewAccountButton.draw(window)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: # Work out where the user clicked and if something should happen (Did they click a button?)
                mousePos = pygame.mouse.get_pos()
                if signInButton.isOver(window, mousePos):
                    running = signIn(window, slotOne, slotTwo)
                elif signUpButton.isOver(window, mousePos):
                    running = signUp(window, slotOne, slotTwo)
                elif signOutButton.isOver(window, mousePos):
                    running = signOut(window, slotOne, slotTwo)
                elif viewAccountButton.isOver(window, mousePos):
                    running = viewAccount(window, slotOne, slotTwo)
                elif backButton.isOver(window, mousePos):
                    return
    return

def signIn(window, slotOne, slotTwo):
    running = True
    while running:
        returnValue = ChooseSlotWindow.chooseSlot(window, slotOne, slotTwo)
        if returnValue != True:
            chosenSlot = returnValue
            if chosenSlot.getAccountID() == None: # Check the slot is available (an account is not already signed into it)
                correctUsernameAndPassword = False  # Run until a correct username & password have been submitted
                while not correctUsernameAndPassword:
                    returnValue = GetUsernameAndPasswordWindow.getUsernameAndPassword(window, "Sign In", slotOne, slotTwo)
                    if returnValue != True: # A username and password was submitted, (else continue loop)
                        returnValue = chosenSlot.signIn(returnValue[0], returnValue[1])
                        if returnValue == None:
                            returnValue = DisplayMessageWindow.displayMessage(window, True, True, "No Account With That Username or Password")
                            if not returnValue: # Back to menu button was clicked, otherwise continue loop
                                return False
                        else:
                            DisplayMessageWindow.displayMessage(window, False, True, "Account Signed In Successfully!")
                            return False
                    else:
                        correctUsernameAndPassword = True # End loop so goes back to ChooseSlotWindow (loop restarts)
            else: # Slot not available - display error message then continue loop when back button clicked
                DisplayMessageWindow.displayMessage(window, True, False, "Account Already Signed into This Slot")
        elif returnValue: # Back button was clicked, return to account area window
            return True
        
def signUp(window, slotOne, slotTwo):
    returnValue = GetUsernameAndPasswordWindow.getUsernameAndPassword(window, "Sign Up", slotOne, slotTwo)
    if returnValue != True: # Add new account if a username and password was returned
        slotOne.signUp(returnValue[0], returnValue[1]) # Use slot object to create account in the database
        returnValue = DisplayMessageWindow.displayMessage(window, False, True, "Account Created!")
        if returnValue == False: # False means back to menu button was clicked - stop accountAreaWindow running
            return False
    elif returnValue: # True = back button was clicked, go back to previous page/window
        return True

def signOut(window, slotOne, slotTwo):
    returnValue = ChooseSlotWindow.chooseSlot(window, slotOne, slotTwo) # choose slot to sign out
    if returnValue != True:
        returnValue.signOut()
        returnValue = DisplayMessageWindow.displayMessage(window, False, True, "Account Signed Out!")
        if returnValue == False: # False means back to menu button was clicked - stop accountAreaWindow running
            return False
    elif returnValue: # True = back button was clicked, go back to previous page/window
        return True

def viewAccount(window, slotOne, slotTwo): 
    # Choose a slot to see the stats stored about the account (view the account)
    running = True
    while running:
        returnValue = ChooseSlotWindow.chooseSlot(window, slotOne, slotTwo) 
        if returnValue != True:
            chosenSlot = returnValue
            if chosenSlot.getAccountID() != None:
                # Display page with the account information/stats on it
                displayStats = True
                while displayStats:
                    window.blit(MENU_BACKGROUND_IMAGE, (0,0))

                    # Display Back Button
                    backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
                    backButton.draw(window)

                    # Display account stats
                    titleFont = pygame.font.SysFont("britannic", int(WIDTH*0.05))
                    titleText = "Account Stats: " + str(chosenSlot.getUsername())
                    title = titleFont.render(titleText, 1, BEIGE)
                    window.blit(title, title.get_rect(center=(WIDTH*0.5, HEIGHT*0.05)))

                    font = pygame.font.SysFont("britannic", int(WIDTH*0.025))

                    statsToDisplay = []

                    statsToDisplay.append("Account Creation Date: " + str(chosenSlot.getAnAccountStat("Date Created")))

                    statsToDisplay.append("Total Number of Wins Against AI: " + str(chosenSlot.getAnAccountStat("Total Number of Wins Against AI")))
                    statsToDisplay.append("Total Number of Draws Against AI: " + str(chosenSlot.getAnAccountStat("Total Number of Draws Against AI")))
                    statsToDisplay.append("Total Number of Losses Against AI: " + str(chosenSlot.getAnAccountStat("Total Number of Losses Against AI")))
                    statsToDisplay.append("Total Number of Games Played Against AI: " + str(chosenSlot.getAnAccountStat("Total Number of Games Played Against AI")))
                    statsToDisplay.append("Highest Win Streak Against AI: " + str(chosenSlot.getAnAccountStat("Highest Win Streak Against AI")))
                    statsToDisplay.append("Current Win Streak Against AI " + str(chosenSlot.getAnAccountStat("Current Win Streak Against AI")))
                    statsToDisplay.append("Average Number of Moves to Win Against AI: " + str(chosenSlot.getAnAccountStat("Average Number of Moves to Win Against AI")))

                    statsToDisplay.append("Total Number of Wins Against Players: " + str(chosenSlot.getAnAccountStat("Total Number of Wins Against Players")))
                    statsToDisplay.append("Total Number of Draws Against Players: " + str(chosenSlot.getAnAccountStat("Total Number of Draws Against Players")))
                    statsToDisplay.append("Total Number of Losses Against Players: " + str(chosenSlot.getAnAccountStat("Total Number of Losses Against Players")))
                    statsToDisplay.append("Total Number of Losses Against Players: " + str(chosenSlot.getAnAccountStat("Total Number of Losses Against Players")))
                    statsToDisplay.append("Highest Win Streak Against Players: " + str(chosenSlot.getAnAccountStat("Highest Win Streak Against Players")))
                    statsToDisplay.append("Current Win Streak Against Players: " + str(chosenSlot.getAnAccountStat("Current Win Streak Against Players")))
                    statsToDisplay.append("Average Number of Moves to Win Against Players: " + str(chosenSlot.getAnAccountStat("Average Number of Moves to Win Against Players")))

                    heightPercentage = 0.1 # Used to calculate height to display stat at
                    for stat in statsToDisplay:
                        renderStat = font.render(stat, 1, BEIGE)
                        window.blit(renderStat, (WIDTH*0.05, HEIGHT*heightPercentage))
                        heightPercentage += 0.05 # Increase height percentage so next stat is lower down
                    
                    pygame.display.flip()

                    # Event handling:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                            quit() # End the program
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mousePos = pygame.mouse.get_pos()
                            if backButton.isOver(window, mousePos):
                                displayStats = False



            else:
                # Display error message and continue loop (go back to choose slot window)
                DisplayMessageWindow.displayMessage(window, True, False, "Slot Empty")
        elif returnValue: # True = back button was clicked, go back to previous page/window
            return True