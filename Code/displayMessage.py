import pygame
import ButtonClass
from Constants import (
    WIDTH, 
    HEIGHT, 
    BACK_BUTTON_WIDTH,
    BACK_BUTTON_HEIGHT,
    BACK_BUTTON_X,
    BACK_BUTTON_Y, 
    BEIGE,
    MENU_BACKGROUND_IMAGE
)


def displayMessage(window, enableBackButton, enableBackToMenuButton, text):
    running = True

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        messageFont = pygame.font.SysFont("britannic", int(WIDTH*0.04)) # Get font using system fonts
        message = messageFont.render(text, 1, BEIGE)
        window.blit(message, message.get_rect(center=(WIDTH*0.5, HEIGHT*0.5)))

        if enableBackButton:
            backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
            backButton.draw(window)

        if enableBackToMenuButton and not enableBackButton:
            backToMenuButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back to Menu")
            backToMenuButton.draw(window)

        if enableBackToMenuButton and enableBackButton:
            backToMenuButton = ButtonClass.Button(BEIGE, (WIDTH-BACK_BUTTON_X-BACK_BUTTON_WIDTH), BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back to Menu")
            backToMenuButton.draw(window)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: # Work out where the user clicked and if something should happen (Did they click a button?)
                mousePos = pygame.mouse.get_pos()
                if enableBackButton:
                    if backButton.isOver(window, mousePos):
                        return True
                if enableBackToMenuButton:
                    if backToMenuButton.isOver(window, mousePos):
                        return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True