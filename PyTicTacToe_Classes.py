import pygame
#from fonts import *

class Board:
    def __init__(self, columns, rows):
        self.numColumns = columns
        self.numRows = rows
        self.BoardSquares = []

        #when this is initialized we need to build a matrix of BoardSquares
        # loop through the rows from top to bottom
        for i in range(0, rows):
            # loop through the columns from left to right
            for j in range(0, columns):
                #since we want to build the squares left to right, top to bottom, use the column loop variable then add to it the row loop variable * rows
                self.BoardSquares.append(BoardSquare(j+(i*rows)))

    def getPieceAtPosition(self, position):
        return self.BoardSquares[position].getGamePiece

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

        # loop through the rows from top to bottom
        for i in range(0, self.numRows):
            # adjust the top left Y coordinate of each board square
            boardSquareY = self.Y + (proportionedPanelSize * i)

            # loop through the columns from left to right
            for j in range(0, self.numColumns):
                # adjust the top left X coordinate point of each board square
                boardSquareX = self.X + (proportionedPanelSize * j)

                # since we want to build the squares left to right, top to bottom, use the column loop variable then add to it the row loop variable * rows
                self.PhysicalBoardSquares.append(PhysicalBoardSquare(j + (i * rows),boardSquareX,boardSquareY,boardSquareSize,boardSquareSize))

    @property
    def getPhysicalBoardSquares(self):
        return self.PhysicalBoardSquares

    def getPieceAtPosition(self, position):
        gamePiece = self.PhysicalBoardSquares[position].getGamePiece
        if gamePiece is not None:
            return gamePiece
        else:
            return GamePiece('Empty')

    def draw(self, gameDisplay, color):
        pygame.draw.rect(gameDisplay, color, (self.X, self.Y, self.width, self.height))

    def drawPhysicalBoardSquares(self, gameDisplay, squareColor):
        for PhysicalBoardSquare in self.PhysicalBoardSquares:
            PhysicalBoardSquare.draw(gameDisplay, squareColor)


    def printMe(self):
        for PhysicalBoardSquare in self.PhysicalBoardSquares:
            if PhysicalBoardSquare.gamePiece is None:
                print('Position: ' + str(PhysicalBoardSquare.position) + ' ' + str(PhysicalBoardSquare.X) + ' ' + str(PhysicalBoardSquare.Y))
            else:
                print('Position: ' + str(PhysicalBoardSquare.position) + ' ' + str(PhysicalBoardSquare.X) + ' ' + str(PhysicalBoardSquare.Y) + ' ' + str(PhysicalBoardSquare.gamePiece.type))


class BoardSquare():
    def __init__(self, position,gamePiece=None):
        self.position = position
        self.gamePiece = gamePiece

    @property
    def getGamePiece(self):
        return self.gamePiece


class PhysicalBoardSquare(BoardSquare):
    def __init__(self, position, X, Y, width, height, gamePiece=None):
        super().__init__(position, gamePiece)

        self.X = X
        self.Y = Y
        self.width = width
        self.height = height
        self.font = pygame.font.Font("fonts/freesansbold.ttf", 80)

    def draw(self, gameDisplay, squareColor):
        pygame.draw.rect(gameDisplay, squareColor, (self.X, self.Y, self.width, self.height))

        if self.gamePiece != None:

            textSurface = self.font.render(self.gamePiece.type, True, self.gamePiece.color)
            textRect = textSurface.get_rect()

            #draw the piece in the center of the square
            textRect.center = (self.X + self.width / 2), (self.Y + self.height / 2)

            gameDisplay.blit(textSurface, textRect)


class GamePiece():
    def __init__(self, type, color=None):
        if type in ('O', 'X', 'Empty'):
            self.type = type
            self.color = color
        else:
            raise ValueError('TicTacToe piece must either be an X or an O')

        @property
        def pieceType(self):
            if self.type != None:
                return self.type
            else:
                return 'Empty!'


class Player():
    def __init__(self, type, playerNum, gamePiece, searchDepth=None, evalFunctionVersion=None):
        if type in ('Human', 'AI'):
            self.type = type
            self.playerNum = playerNum
            self.gamePiece = gamePiece
            self.searchDepth = searchDepth
            self.evalFunctionVersion = evalFunctionVersion
            self.gamesWon = 0
        else:
            raise ValueError('Player type must be a Human or an AI')


#represents one move of a single piece
class Move():
    def __init__(self, gamePiece, newPosition):
        self.gamePiece = gamePiece
        self.newPosition = newPosition


#represents one player's turn and the number of moves made in that turn
class Turn():
    def __init__(self, turnNum, currentPlayer):
        self.turnNum = turnNum
        self.player = currentPlayer
        self.moves = []
        
#should Game have a physical game board or a game board?
#in the future we'll need to check for winners in virtual boards, so the physical board game calls in the isWinner* functions kind of destroy that
class Game():
    def __init__(self, aiDifficulty=None):
        self.aiDifficulty = aiDifficulty
        self.physicalGameBoard = None
        self.gameState = 'In Progress'
        self.gameWinner = None
        self.Players = []
        self.Turns = []

        #for TicTacToe the length required to win is 3
        self.WINNING_LENGTH = 3

    def getOpponent(self, player):
        if len(self.Players) != 2:
            raise ValueError('This game doesn''t have 2 players')

        #return the opposite player
        if player.playerNum == 1:
            return self.Players[1]
        elif player.playerNum == 2:
            return self.Players[0]

    #decouple from physical..
    def isWinnerFromTopToBottom(self,position):
        if self.physicalGameBoard is None:
            return False

        #if the position is greater than the number of 2 then ??
        if position > 2:
            return False
        else:
            gamePiece = self.physicalGameBoard.getPieceAtPosition(position)
            if (gamePiece is None) or (gamePiece.type == 'Empty'):
                return False

            #for PhysicalBoardSquare in self.physicalGameBoard.PhysicalBoardSquares:
            for i in range(1, self.WINNING_LENGTH):
                if gamePiece.type != self.physicalGameBoard.getPieceAtPosition(position + 3 * i).type:
                    return False

            return True
        