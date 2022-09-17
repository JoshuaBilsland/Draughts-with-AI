import pygame
import ButtonClass
import ChooseSlot
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

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: # Work out where the user clicked and if something should happen (Did they click a button?)
                mousePos = pygame.mouse.get_pos()
                if signInButton.isOver(window, mousePos):
                    signIn(window, slotOne, slotTwo)
                elif signUpButton.isOver(window, mousePos):
                    print("Sign up")
                elif signOutButton.isOver(window, mousePos):
                    print("Sign out")
                elif viewAccountButton.isOver(window, mousePos):
                    print("View Account")
                elif backButton.isOver(window, mousePos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def signIn(window, slotOne, slotTwo):
    chosenSlot = ChooseSlot.chooseSlot(window, slotOne, slotTwo)