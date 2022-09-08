import pygame
import ButtonClass
import DatabaseClass
import GameWindow
import AccountArea
from Constants import (
    WIDTH,
    HEIGHT, 
    REGULAR_BUTTON_WIDTH, 
    REGULAR_BUTTON_HEIGHT,
    REGULAR_BUTTON_X,
    REGULAR_BUTTON_Y,
    BEIGE, 
    MENU_BACKGROUND_IMAGE
)


# Setup the window
pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT))

def mainMenuWindow(slotOne, slotTwo):
    running = True

    while running:
        # Draw/Make the main menu 
        window.blit(MENU_BACKGROUND_IMAGE, (0, 0))
        
        mainTitleFont = pygame.font.SysFont("britannic", int(WIDTH*0.1)) # Use system fonts
        mainTitle = mainTitleFont.render("Draughts With AI", 1, BEIGE)
        window.blit(mainTitle, mainTitle.get_rect(center=(WIDTH/2, 50))) # Centre the text on its own rect
        
        startGameButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+100, REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Start Game") # Creates start game button
        startGameButton.draw(window)
        
        accountsButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+100+(HEIGHT*0.2), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Account") # Created quit button
        accountsButton.draw(window)
        
        quitButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+100+(HEIGHT*0.4), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Quit") # Created quit button
        quitButton.draw(window)

        pygame.display.flip()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: # Work out where the user clicked and if something should happen (Did they click a button?)
                mousePos = pygame.mouse.get_pos()
                if startGameButton.isOver(window, mousePos):
                    slots = GameWindow.gameWindow(window,  slotOne, slotTwo) # slots are returned, slots are passed around each subroutine in the game
                elif accountsButton.isOver(window, mousePos):
                    slots = AccountArea.accountAreaWindow(window, slotOne, slotTwo)  # slots are returned, slots are passed around each subroutine in the game
                elif quitButton.isOver(window, mousePos):
                    running = False

# Main
slotOne = Account.account()
slotTwo = Account.account()

mainMenuWindow(slotOne, slotTwo)
