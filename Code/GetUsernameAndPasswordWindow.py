import pygame
import ButtonClass
from Constants import (
    MENU_BACKGROUND_IMAGE,
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK,
    BEIGE,
    REGULAR_BUTTON_HEIGHT,
    REGULAR_BUTTON_WIDTH,
    REGULAR_BUTTON_X,
    REGULAR_BUTTON_Y,
    BACK_BUTTON_HEIGHT,
    BACK_BUTTON_WIDTH,
    BACK_BUTTON_X,
    BACK_BUTTON_Y
)

def getUsernameAndPassword(window, textForButton, slotOne, slotTwo):
    running = True
    
    inputFont = pygame.font.SysFont("britannic", 20) # Set font for text the user enters

    # Text is only entered in to a field/box if it is selected (The user has clicked on it), Start with neither selected
    usernameInputSelected = False
    passwordInputSelected = False
    
    # Create the rect objects which text is 'entered in to' (displayed on)
    usernameInputBox = pygame.Rect(WIDTH*0.125, HEIGHT*0.2, WIDTH*0.75, 40)
    passwordInputBox = pygame.Rect(WIDTH*0.125, HEIGHT*0.5, WIDTH*0.75, 40)

    # Strings for storing user input
    usernameInputString = ""
    passwordInputString = ""
    passwordInputStringHidden = ""

    # Allow keys/backspace to be held down
    pygame.key.set_repeat(250,150)

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        # Generate hidden version of password
        passwordInputStringHidden = ""
        for char in passwordInputString:
            passwordInputStringHidden += "*"

        # Draw buttons
        mainButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X, REGULAR_BUTTON_Y+(HEIGHT*0.55), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT*0.75, textForButton)
        mainButton.draw(window)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)

        # Draw username and password headings
        headingFont = pygame.font.SysFont("britannic", int(WIDTH*0.08)) # Get font using system fonts
        usernameHeading = headingFont.render("Username", 1, BEIGE)
        passwordHeading = headingFont.render("Password", 1, BEIGE)
        window.blit(usernameHeading, usernameHeading.get_rect(center=(WIDTH*0.5, HEIGHT*0.1)))
        window.blit(passwordHeading, passwordHeading.get_rect(center=(WIDTH*0.5, HEIGHT*0.4)))

        # Draw the text input boxes
        pygame.draw.rect(window, WHITE, usernameInputBox)
        pygame.draw.rect(window, WHITE, passwordInputBox)

        # Create text surface objects
        usernameInput = inputFont.render(usernameInputString, True, BLACK)
        passwordInput = inputFont.render(passwordInputStringHidden, True, BLACK)

        # Draw the text onto the boxes/fields (+5 & +10 used to better position the text inside the box)
        window.blit(usernameInput, (usernameInputBox.x + 5, usernameInputBox.y + 10)) 
        window.blit(passwordInput, (passwordInputBox.x + 5, passwordInputBox.y + 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program

            elif event.type == pygame.MOUSEBUTTONDOWN: # Check if the user clicked on an input box - select it so they can enter text in to it
                mousePos = pygame.mouse.get_pos()
                if mainButton.isOver(window, mousePos):
                    return usernameInputString, passwordInputString
                elif backButton.isOver(window, mousePos):
                    return True
                elif usernameInputBox.collidepoint(mousePos):
                    usernameInputSelected = True
                    passwordInputSelected = False
                elif passwordInputBox.collidepoint(mousePos):
                    passwordInputSelected = True
                    usernameInputSelected = False
                else:
                    usernameInputSelected, passwordInputSelected = False, False

            elif event.type == pygame.KEYDOWN: # add the users text to the strings
                if usernameInputSelected:
                    if event.key == pygame.K_BACKSPACE: # Delete the last character of the string
                        usernameInputString = usernameInputString[:-1]
                    elif usernameInput.get_width() < (usernameInputBox.width-30):
                        usernameInputString += event.unicode
                elif passwordInputSelected:
                    if event.key == pygame.K_BACKSPACE: # Delete the last character of the string
                        passwordInputString = passwordInputString[:-1]
                    elif passwordInput.get_width() < (passwordInputBox.width-10):
                        passwordInputString += event.unicode
