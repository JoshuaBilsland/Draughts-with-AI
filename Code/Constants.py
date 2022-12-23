import pygame


# Window
WIDTH = 800
HEIGHT = 800

# Button
REGULAR_BUTTON_WIDTH= int(WIDTH*0.4)
REGULAR_BUTTON_HEIGHT = int(HEIGHT*0.15)
REGULAR_BUTTON_X = int((WIDTH*0.5)-REGULAR_BUTTON_WIDTH*0.5)
REGULAR_BUTTON_Y = int(HEIGHT*0.1)

BACK_BUTTON_WIDTH = int(WIDTH*0.2)
BACK_BUTTON_HEIGHT = int(HEIGHT*0.1)
BACK_BUTTON_X = int(WIDTH*0.05)
BACK_BUTTON_Y = int(HEIGHT*0.87) 

# RGB
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
BEIGE = (226,201,158)
BROWN = (175,135,67)
BLUE = (50,175,255)
RED = (255,0,0)

# Colour for men
COLOUR_ONE = BLACK
COLOUR_TWO = WHITE

# Board
ROWS = 8
COLUMNS = 8
SQUARE_SIZE = WIDTH / COLUMNS

# Images
MENU_BACKGROUND_IMAGE = pygame.image.load("Images\\WoodMenuBackground.png")
CROWN = pygame.transform.scale(pygame.image.load("Images\\Crown.png"), (SQUARE_SIZE, SQUARE_SIZE/2))
