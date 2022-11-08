import pygame
import ButtonClass
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

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        # Choose colour to play as
        manColourOneButton = ButtonClass.Button(COLOUR_ONE, REGULAR_BUTTON_X-(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.1), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "")
        manColourOneButton.draw(window)
        if manColourOneButtonSelected == True:
            manColourOneButton.drawSelectedLines(window, RED)

        manColourTwoButton = ButtonClass.Button(COLOUR_TWO, REGULAR_BUTTON_X+(WIDTH/4), REGULAR_BUTTON_Y+(HEIGHT*0.1), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "")
        manColourTwoButton.draw(window)
        if manColourTwoButtonSelected == True:
            manColourTwoButton.drawSelectedLines(window, RED)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)
        
        if gameMode == "PvP":
            font = pygame.font.SysFont("britannic", int(WIDTH*0.04)) # Get font using system fonts
            instructionText = font.render("Choose Slot One's Colour", 1, BEIGE)
            window.blit(instructionText, instructionText.get_rect(center=(WIDTH*0.5, HEIGHT*0.1))) # Centre the text on its own rect

        else: # gameMode == "PvAI"
            font = pygame.font.SysFont("britannic", int(WIDTH*0.04)) # Get font using system fonts
            instructionText = font.render("Choose Colour To Play As", 1, BEIGE)
            window.blit(instructionText, instructionText.get_rect(center=(WIDTH*0.5, HEIGHT*0.1))) # Centre the text on its own rect            

        pygame.display.flip()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mousePos = pygame.mouse.get_pos()
                if manColourOneButton.isOver(window, mousePos):
                    # 'Select' colour -> draw red border lines to show it is selected
                    manColourOneButtonSelected = True
                    manColourTwoButtonSelected = False
                elif manColourTwoButton.isOver(window, mousePos):
                    # 'Select' colour -> draw red border lines to show it is selected
                    manColourTwoButtonSelected = True
                    manColourOneButtonSelected = False
                elif backButton.isOver(window, mousePos): # Return true as back button was pressed
                    return True