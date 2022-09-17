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

# Gets the user to choose which slot they want to sign in/out, view
def chooseSlot(window, slotOne, slotTwo):
    running = True

    while running:
        window.blit(MENU_BACKGROUND_IMAGE, (0,0))

        slotOneButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X+(WIDTH*0.25), REGULAR_BUTTON_Y+(HEIGHT*0.5), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Slot One")
        slotOneButton.draw(window)

        slotTwoButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X+(WIDTH*0.75), REGULAR_BUTTON_Y+(HEIGHT*0.5), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Slot Two")
        slotTwoButton.draw(window)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)

        pygame.display.flip()