import pygame
from Constants import (
    WHITE, 
    BLACK
)

class Button():
    def __init__(self, colour, x, y, width, height, text):
        self.__colour = colour
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__text = text

    # Other
    def draw(self, window): # Draw the button onto a window
        pygame.draw.rect(window, self.__colour, (self.__x, self.__y, self.__width, self.__height), 0)
        # Draw 3D edge effect
        pygame.draw.line(window, WHITE, (self.__x, self.__y), (self.__x + self.__width, self.__y),2)
        pygame.draw.line(window, WHITE, (self.__x, self.__y), (self.__x, self.__y + self.__height), 2)
        pygame.draw.line(window, BLACK, (self.__x, self.__y + self.__height), (self.__x + self.__width, self.__y + self.__height), 2)
        pygame.draw.line(window, BLACK, (self.__x + self.__width, self.__y), (self.__x + self.__width, self.__y + self.__height), 2)
        
        if self.__text == "Back":
            font = pygame.font.SysFont("britannic", int(self.__width*0.2)) # Use system fonts
            text = font.render(self.__text, 1, BLACK)  # Apply font settings to the text  
            window.blit(text, (self.__x + (self.__width/2 - text.get_width()/2), self.__y + (self.__height/2 - text.get_height()/2)))
        
        elif self.__text != "":
            font = pygame.font.SysFont("britannic", int(self.__width*0.1)) # Use system fonts
            text = font.render(self.__text, 1, BLACK)  # Apply font settings to the text  
            window.blit(text, (self.__x + (self.__width/2 - text.get_width()/2), self.__y + (self.__height/2 - text.get_height()/2)))


    
    def isOver(self, window, mousePos):  # Checks if a position is within the area of the button (Used to see if the button has been clicked)
        if mousePos[0] > self.__x and mousePos[0] < self.__x + self.__width:
            if mousePos[1] > self.__y and mousePos[1] < self.__y + self.__height:
                return True
        return False 


    


