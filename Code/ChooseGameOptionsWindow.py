import pygame
import ButtonClass
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
    RED,
    COLOUR_ONE,
    COLOUR_TWO,
    MENU_BACKGROUND_IMAGE
)

# Get the user to choose the game mode they want to play
def chooseGameOptions(window, gameMode, slotOne, slotTwo):
    running = True
    manColourOneButtonSelected = False
    manColourTwoButtonSelected = False
    difficultySelected = None # 1 == Easy, 2 == Average, 3 == Hard, 4 == Expert

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        # Choose colour to play as
        manColourOneButton = ButtonClass.Button(COLOUR_ONE, REGULAR_BUTTON_X-(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.07), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "")
        manColourOneButton.draw(window)
        if manColourOneButtonSelected == True:
            manColourOneButton.drawSelectedLines(window, RED)

        manColourTwoButton = ButtonClass.Button(COLOUR_TWO, REGULAR_BUTTON_X+(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.07), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "")
        manColourTwoButton.draw(window)
        if manColourTwoButtonSelected == True:
            manColourTwoButton.drawSelectedLines(window, RED)

        startButton = ButtonClass.Button(BEIGE, (WIDTH-BACK_BUTTON_X-BACK_BUTTON_WIDTH), BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Start")
        startButton.draw(window)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)
        
        if gameMode == "PvP":
            font = pygame.font.SysFont("britannic", int(WIDTH*0.04)) # Get font using system fonts
            chooseColourText = font.render("Choose Slot One's Colour", 1, BEIGE)
            window.blit(chooseColourText, chooseColourText.get_rect(center=(WIDTH*0.5, HEIGHT*0.1))) # Centre the text on its own rect

        else: # gameMode == "PvAI"
            font = pygame.font.SysFont("britannic", int(WIDTH*0.04)) # Get font using system fonts
            chooseColourText = font.render("Choose Colour To Play As", 1, BEIGE)
            window.blit(chooseColourText,   chooseColourText.get_rect(center=(WIDTH*0.5, HEIGHT*0.1))) # Centre the text on its own rect

            # Title + Buttons for choosing the difficulty of the AI
            chooseDifficultyText = font.render("Select Difficulty", 1, BEIGE)  
            window.blit(chooseDifficultyText, chooseDifficultyText.get_rect(center=(WIDTH*0.5, HEIGHT*0.42))) # Centre the text on its own rect          
            easyButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X-(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.4), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Easy")
            easyButton.draw(window)
            averageButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X+(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.4), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Average")
            averageButton.draw(window)
            hardButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X-(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.58), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Hard")
            hardButton.draw(window)
            expertButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X+(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.58), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Expert")
            expertButton.draw(window)

            # Draw lines on the selected difficulty
            if difficultySelected == 1:
                easyButton.drawSelectedLines(window, RED)
            elif difficultySelected == 2:
                averageButton.drawSelectedLines(window, RED)
            elif difficultySelected == 3:
                hardButton.drawSelectedLines(window, RED)
            elif difficultySelected == 4:
                expertButton.drawSelectedLines(window, RED)

        pygame.display.flip()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mousePos = pygame.mouse.get_pos()
                if gameMode == "PvAI":
                    if easyButton.isOver(window, mousePos):
                        difficultySelected = 1
                    elif averageButton.isOver(window, mousePos):
                        difficultySelected = 2
                    elif hardButton.isOver(window, mousePos):
                        difficultySelected = 3 
                    elif expertButton.isOver(window, mousePos):
                        difficultySelected = 4
                if manColourOneButton.isOver(window, mousePos):
                    # 'Select' colour -> draw red border lines to show it is selected
                    manColourOneButtonSelected = True
                    manColourTwoButtonSelected = False
                elif manColourTwoButton.isOver(window, mousePos):
                    # 'Select' colour -> draw red border lines to show it is selected
                    manColourTwoButtonSelected = True
                    manColourOneButtonSelected = False
                elif startButton.isOver(window, mousePos):
                    if areStartGameRequirementsMet(gameMode, manColourOneButtonSelected, manColourTwoButtonSelected, difficultySelected):
                        chosenOptions = [] # Used to store data to return
                        if manColourOneButtonSelected == True:
                            chosenOptions.append("C1") # Colour one was chosen
                        else:
                            chosenOptions.append("C2") # Colour two was chosen
                        if gameMode == "PvAI":
                            chosenOptions.append(difficultySelected)
                        return chosenOptions # Return the options that the user has chosen - Used to setup the game
                    else:
                        DisplayMessageWindow.displayMessage(window, True, False, "Check You Have Chosen The Required Game Options")
                elif backButton.isOver(window, mousePos): # Return true as back button was pressed
                    return True

def areStartGameRequirementsMet(gameMode, manColourOneButtonSelected, manColourTwoButtonSelected, difficultySelected): # Check that the user has chosen the required options to play - A colour to play as, etc
    requirementsMet = False
    if manColourOneButtonSelected == True or manColourTwoButtonSelected == True:
        if gameMode == "PvP":
            requirementsMet = True
        else: # gameMode == "PvAI"
            if difficultySelected != None:
                requirementsMet = True
    return requirementsMet
