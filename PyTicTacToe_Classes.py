import pygame
import colors as c

class Board:
    def __init__(self, columns, rows):
        self.numColumns = columns
        self.numRows = rows
        self.BoardSquares = []

        #when this is initialized we need to build a matrix of BoardSquares
        # loop through the columns from left to right
        for i in range(0, columns):
            # adjust the top left X coordinate point of each board square
            #boardSquareX = panelX + (proportionedPanelSize * i)

            # loop through the rows from top to bottom
            for j in range(0, rows):
                # adjust the top left Y coordinate of each board square
                #boardSquareY = panelY + (proportionedPanelSize * j)
                #pygame.draw.rect(gameDisplay, red, (boardSquareX, boardSquareY, boardSquareSize, boardSquareSize))

                #since we want to build the squares left to right, top to bottom, use the row loop variable then add to it the column loop variable * cols
                self.BoardSquares.append(BoardSquare(j+(i*columns)))

    def printMe(self):
        for BoardSquare in self.BoardSquares:
            print('Position: ' + str(BoardSquare.position))


class PhysicalBoard(Board):
    def __init__(self, columns, rows, X, Y, width, height):
        super().__init__(columns, rows)

        self.X = X
        self.Y = Y
        self.width = width
        self.height = height
        self.PhysicalBoardSquares = []

        # make the board square 6 pixels less than 1/3 the size of the panel so we can fit 3 across and 3 down
        boardSquareSize = int((self.width / 3) - 6)

        #generate physical board squares
        #add 2 pixels to a proportion of the panel width
        proportionedPanelSize = int(self.width / self.numColumns) + 2

        boardSquareX = self.X
        boardSquareY = self.Y

        # loop through the columns from left to right
        for i in range(0, self.numColumns):
            #adjust the top left X coordinate point of each board square
            boardSquareX = self.X + (proportionedPanelSize * i)

            # loop through the rows from top to bottom
            for j in range(0, self.numRows):
                # adjust the top left Y coordinate of each board square
                boardSquareY = self.Y + (proportionedPanelSize * j)
                # pygame.draw.rect(gameDisplay, red, (boardSquareX, boardSquareY, boardSquareSize, boardSquareSize))

                # since we want to build the squares left to right, top to bottom, use the row loop variable then add to it the column loop variable * cols
                self.PhysicalBoardSquares.append(PhysicalBoardSquare(j + (i * columns),boardSquareX,boardSquareY,boardSquareSize,boardSquareSize))

    def draw(self, gameDisplay, color):
        pygame.draw.rect(gameDisplay, color, (self.X, self.Y, self.width, self.height))

    def drawBoardSquares(self, gameDisplay, color):
        pass

    def printMe(self):
        for PhysicalBoardSquare in self.PhysicalBoardSquares:
            print('Position: ' + str(PhysicalBoardSquare.position) + ' ' + str(PhysicalBoardSquare.X) + ' ' + str(PhysicalBoardSquare.Y))



class BoardSquare():
    def __init__(self, position):
        self.position = position

class PhysicalBoardSquare(BoardSquare):
    def __init__(self, position, X, Y, width, height):
        super().__init__(position)

        self.X = X
        self.Y = Y
        self.width = width
        self.height = height

    def draw(self, gameDisplay, color):
        pygame.draw.rect(gameDisplay, color, (self.X, self.Y, self.width, self.height))