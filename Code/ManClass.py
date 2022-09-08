import pygame
from Constants import (
    SQUARE_SIZE, 
    CROWN
)


class Man():
    __row = None
    __column = None
    __colour = None
    __isKing = False
    __x = None
    __y = None

    def __init__(self, row, column, colour):
        self.__row = row
        self.__column = column
        self.__colour = colour
        self.__x = self.determineX()
        self.__y = self.determineY()

    def determineX(self):
        x = SQUARE_SIZE * self.__column + SQUARE_SIZE / 2
        return x

    def determineY(self):
        y = SQUARE_SIZE * self.__row + SQUARE_SIZE / 2
        return y

    def getRow(self):
        return self.__row

    def getColumn(self):
        return self.__column

    def getColour(self):
        return self.__colour
        
    def makeKing(self): # Turn a man into a king
        self.__isKing = True
        self.draw() # Redrawing the man will now also draw the crown since isKing = True

    def draw(self, window):
        radius = (SQUARE_SIZE / 2) - 10
        pygame.draw.circle(window, self.__colour, (self.__x, self.__y), radius)
        if self.__isKing == True:
            window.blit(CROWN, (self.__x - CROWN.get_width()/2, self.__y - CROWN.get_height()/2))

    def move(self, row, column):
        self.__row = row
        self.__column = column
        self.__x = self.determineX()
        self.__y = self.determineY()
