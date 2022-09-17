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

        slotOneButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X-(HEIGHT*0.25), REGULAR_BUTTON_Y+(HEIGHT*0.3), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Slot One")
        slotOneButton.draw(window)

        slotTwoButton = ButtonClass.Button(BEIGE, REGULAR_BUTTON_X+(HEIGHT*0.25), REGULAR_BUTTON_Y+(HEIGHT*0.3), REGULAR_BUTTON_WIDTH, REGULAR_BUTTON_HEIGHT, "Slot Two")
        slotTwoButton.draw(window)

        backButton = ButtonClass.Button(BEIGE, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, "Back")
        backButton.draw(window)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            elif event.type == pygame.MOUSEBUTTONDOWN: # Work out where the user clicked and if something should happen (Did they click a button?)
                mousePos = pygame.mouse.get_pos()
                if slotOneButton.isOver(window, mousePos): # Return slotOne as the chosen slot
                    return slotOne
                elif slotTwoButton.isOver(window, mousePos): # Return slotTwo as the chosen slot
                    return slotTwo
                elif backButton.isOver(window, mousePos): # Return 
                    return None