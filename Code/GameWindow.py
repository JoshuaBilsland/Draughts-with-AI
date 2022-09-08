import pygame
import BoardClass
import GameClass
from Constants import (
    COLOUR_ONE, 
    COLOUR_TWO
)

def gameWindow(window,slotOne, slotTwo, run):
    running = run
    game = GameClass.Game(window, [123, COLOUR_ONE], [456, COLOUR_TWO])
    
    while running:
        game.updateDisplay() # Display game window instead of main menu
                          # + keep updating it incase of any changes (For example, a man is moved)
        # Event loop
        if game.getGameFinished() == True:
            quit() # End the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if the close button in the top right is clicked
                quit() # End the program
            if event.type == pygame.MOUSEBUTTONDOWN: # Work out where the user clicked and if something should happen
                mousePos = pygame.mouse.get_pos()
                game.processClick(mousePos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return slotOne, slotTwo, False # Return slotOne and slotTwo in case of changes, True or False
                    
                
                
