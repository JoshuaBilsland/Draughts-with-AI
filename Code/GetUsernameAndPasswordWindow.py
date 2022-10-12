import pygame
import ButtonClass
from Constants import (
    MENU_BACKGROUND_IMAGE,
    WIDTH,
    HEIGHT,
    WHITE
)

def getUsernameAndPassword(window, slotOne, slotTwo):
    running = True
    
    font = pygame.font.SysFont("britannic", 18) # Set font for text the user enters

    # Text is only entered into a field/box if it is selected (The user has clicked on it), Start with neither selected
    usernameInputSelected = False
    passwordInputSelected = False
    
    # Create the rect objects which text is 'entered into' (displayed on)
    usernameInputBox = pygame.Rect(WIDTH*0.1, HEIGHT*0.2, HEIGHT*0.75, 30)
    passwordInputBox = pygame.Rect(WIDTH*0.1, HEIGHT*0.4, HEIGHT*0.75, 30)

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        # Draw the text input boxes
        pygame.draw.rect(window, WHITE, usernameInputBox)
        pygame.draw.rect(window, WHITE, passwordInputBox)

        # The string that the user has entered into the username and password boxes/fields
        usernameInput = font.render("", True, (190,195,205))
        passwordInput = font.render("", True, (190,195,205))

        # Draw the text onto the boxes/fields
        window.blit(usernameInput, usernameInputBox)
        window.blit(passwordInput, passwordInputBox)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program

            elif event.type == pygame.MOUSEBUTTONDOWN: # Check if the user clicked on an input box - select it so they can enter text into it
                mousePos = pygame.mouse.get_pos()
                if usernameInputBox.collidepoint(mousePos):
                    usernameInputSelected = True
                elif passwordInputBox.collidepoint(mousePos):
                    passwordInputSelected = True
                else:
                    usernameInputSelected, passwordInputSelected = False, False

            elif event.type == pygame.KEYDOWN: # add the users text to the strings
                if usernameInputSelected:
                    if event.key == pygame.K_BACKSPACE: # Delete the last character of the string
                        usernameInput = usernameInput[:-1]
                    else:
                        usernameInput += event.unicode
                elif passwordInputSelected:
                    if event.key == pygame.K_BACKSPACE: # Delete the last character of the string
                        passwordInput = passwordInput[:-1]
                    else:
                        passwordInput += event.unicode
        