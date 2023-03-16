import pygame
from Constants import (
    WHITE, 
    BLACK
)

class Button:
    def __init__(self, colour, x, y, width, height, text):
        self.__colour = colour
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__text = text


    # Other Methods

    # Draw the button onto the pygame window
    def draw(self, window):
        pygame.draw.rect(window, self.__colour, (self.__x, self.__y, self.__width, self.__height), 0)
        
        # Draw 3D edge effect -> draw lines on the button so it doesn't just look like a flat rectangle
        if self.__colour != BLACK and self.__colour != WHITE:
            pygame.draw.line(window, WHITE, (self.__x, self.__y), (self.__x + self.__width, self.__y),2)
            pygame.draw.line(window, WHITE, (self.__x, self.__y), (self.__x, self.__y + self.__height), 2)
            pygame.draw.line(window, BLACK, (self.__x, self.__y + self.__height), (self.__x + self.__width, self.__y + self.__height), 2)
            pygame.draw.line(window, BLACK, (self.__x + self.__width, self.__y), (self.__x + self.__width, self.__y + self.__height), 2)

        # These buttons should have the text drawn smaller since the buttons themselves will be smaller
        if self.__text == "Back" or self.__text == "Back to Menu" or self.__text == "Start":
            font = pygame.font.SysFont("britannic", int(self.__width*0.15)) # Use system fonts
            text = font.render(self.__text, True, BLACK)  # Apply font settings to the text  
            window.blit(text, (self.__x + (self.__width/2 - text.get_width()/2), self.__y + (self.__height/2 - text.get_height()/2)))

        
        # Format and add the given text to the button 
        elif self.__text != "": # Buttons with no text are used in ChooseGameOptionsWindow.py to show the choice of colours to play as before a game start (the button is just filled in with one of the available colours)
            font = pygame.font.SysFont("britannic", int(self.__width*0.1)) # Use system fonts
            text = font.render(self.__text, True, BLACK)  # Apply font settings to the text  
            window.blit(text, (self.__x + (self.__width/2 - text.get_width()/2), self.__y + (self.__height/2 - text.get_height()/2)))


    # Checks if a position is within the area of the button (Used to see if the button has been clicked)
    def isOver(self, window, mousePos):
        boolean = False
        if mousePos[0] > self.__x and mousePos[0] < self.__x + self.__width:
            if mousePos[1] > self.__y and mousePos[1] < self.__y + self.__height:
                boolean = True
        return boolean


    # Draw buttons around the button to show it has been selected (used in ChooseGameOptions.py to display which options are currently selected and will be used to create the game object/start the game)
    def drawSelectedLines(self, window, colour):
            pygame.draw.line(window, colour, (self.__x, self.__y), (self.__x + self.__width, self.__y),2)
            pygame.draw.line(window, colour, (self.__x, self.__y), (self.__x, self.__y + self.__height), 2)
            pygame.draw.line(window, colour, (self.__x, self.__y + self.__height), (self.__x + self.__width, self.__y + self.__height), 2)
            pygame.draw.line(window, colour, (self.__x + self.__width, self.__y), (self.__x + self.__width, self.__y + self.__height), 2)        
