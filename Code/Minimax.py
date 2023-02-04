import math
from Constants import(
    COLOUR_ONE,
    COLOUR_TWO
)

def minimax(board, isColourOne, depth, valueKingPromotion):
    pass

def scoreBoard(board): # Take a board object and score it (for the minimax algorithm)
    allManObjects = board.getAllMen() # list of all man objects left on the board
    
    numberOfColourOneMen = 0
    numberOfColourTwoMen = 0
    
    numberOfColourOneKings = 0
    numberOfColourTwoKings = 0

    for man in allManObjects:
        manColour = man.getColour
        manIsKing = man.isKing()
        if manColour == COLOUR_ONE:
            if manIsKing:
                numberOfColourOneKings += 1
            else:
                numberOfColourOneMen += 1
        else:
            if manIsKing:
                numberOfColourTwoKings += 1
            else:
                numberOfColourTwoMen += 1

    score = numberOfColourOneMen - numberOfColourTwoMen
    score += (numberOfColourOneKings - numberOfColourTwoKings)*2
    
    return score


