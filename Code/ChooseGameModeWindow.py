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
    MENU_BACKGROUND_IMAGE
)

# Get the user to choose the game mode they want to play
def chooseGameMode(window, slotOne, slotTwo):
    running = True

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        playerVsPlayerButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+(HEIGHT*0.1), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Player vs Player")
        playerVsPlayerButton.draw(window)

        playerVsAIButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+(HEIGHT*0.4), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Player vs AI")
        playerVsAIButton.draw(window)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)

        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mousePos = pygame.mouse.get_pos()
                if playerVsPlayerButton.isOver(window, mousePos):
                    return "PvP"
                elif playerVsAIButton.isOver(window, mousePos):
                    return "PvAI"
                elif backButton.isOver(window, mousePos): # Return true as back button was pressed
                    return True