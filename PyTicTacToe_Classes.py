import pygame
import abc
import random
#from fonts import *

class Board:
    def __init__(self, columns, rows):
        self.numColumns = columns
        self.numRows = rows
        self.BoardSquares = []
        self.GamePieces = []

        #for TicTacToe the length required to win is 3
        self.WINNING_LENGTH = 3


        #when this is initialized we need to build a matrix of BoardSquares
        # loop through the rows from top to bottom
        for i in range(0, rows):
            # loop through the columns from left to right
            for j in range(0, columns):
                #since we want to build the squares left to right, top to bottom, use the column loop variable then add to it the row loop variable * rows
                #self.BoardSquares.append(BoardSquare(j+(i*rows)))
                self.GamePieces.append(GamePiece('Empty'))

    def getPieceAtPosition(self, position):
        #return self.BoardSquares[position].getGamePiece
        return self.GamePieces[position]

    def printMe(self):
        for BoardSquare in self.BoardSquares:
            print('Position: ' + str(BoardSquare.position))

    def getOpenPositions(self):
        lOpenPositions = []

        for i in range(0, len(self.GamePieces)):
            if not self.getIsPositionOccupied(i):
                lOpenPositions.append(i)

        return lOpenPositions

    def getIsPositionOccupied(self, position):
        return self.GamePieces[position].type != 'Empty'

    def getPoint(self,position):
        pointX = int(position / self.numColumns)
        pointY = position % self.numRows

        return pointX, pointY

    def getPositionFromPoint(self, point):
        return int(point[0] * self.numColumns + point[1])


    def getIsPointInBounds(self, point):
        x = point[0]
        y = point[1]

        if x < 0 or x >= self.numRows or y < 0 or y >= self.numColumns:
            return False

        return True


    def isWinnerFromTopToBottom(self, position):
        #if this position isn't occupied we can't find a winner from it
        if not self.getIsPositionOccupied(position):
            return False

        point = self.getPoint(position)

        #do we have room below us?
        if point[0] + self.WINNING_LENGTH - 1 >= self.numRows:
            return False
        else:
            gamePiece = self.getPieceAtPosition(position)
            # if (gamePiece is None) or (gamePiece.type == 'Empty'):
            #     return False

            for i in range(1, self.WINNING_LENGTH):
                if gamePiece.type != self.getPieceAtPosition(position + 3 * i).type:
                    return False

            return True

    def isWinnerToTheRight(self, position):
        #if this position isn't occupied we can't find a winner from it
        if not self.getIsPositionOccupied(position):
            return False

        point = self.getPoint(position)

        #do we have room to the right?
        if point[1] + self.WINNING_LENGTH - 1 >= self.numColumns:
            return False
        else:
            gamePiece = self.getPieceAtPosition(position)
            # if (gamePiece is None) or (gamePiece.type == 'Empty'):
            #     return False

            for i in range(1, self.WINNING_LENGTH):
                if gamePiece.type != self.getPieceAtPosition(position + i).type:
                    return False

            return True

    def isWinnerDiagonallyDownToRight(self, position):
        #if this position isn't occupied we can't find a winner from it
        if not self.getIsPositionOccupied(position):
            return False

        point = self.getPoint(position)
        x = point[0]
        y = point[1]

        gamePiece = self.getPieceAtPosition(position)

        for i in range(1, self.WINNING_LENGTH):
            x += 1
            y += 1

            if not self.getIsPointInBounds((x,y)):
                return False

            if gamePiece.type != self.getPieceAtPosition(self.getPositionFromPoint((x,y))).type:
                return False

        return True


    def isWinnerDiagonallyUpToRight(self, position):
        #if this position isn't occupied we can't find a winner from it
        if not self.getIsPositionOccupied(position):
            return False

        point = self.getPoint(position)
        x = point[0]
        y = point[1]

        gamePiece = self.getPieceAtPosition(position)

        for i in range(1, self.WINNING_LENGTH):
            x -= 1
            y += 1

            if not self.getIsPointInBounds((x, y)):
                return False

            if gamePiece.type != self.getPieceAtPosition(self.getPositionFromPoint((x, y))).type:
                return False

        return True

    def isWinnerAtPosition(self, position):
        if self.isWinnerToTheRight(position) or self.isWinnerFromTopToBottom(position) or \
                self.isWinnerDiagonallyDownToRight(position) or self.isWinnerDiagonallyUpToRight(position):
            return True
        else:
            return False

    def isThereAWinner(self):
        for i in range(0, len(self.GamePieces)):
            if self.isWinnerAtPosition(i):
                return True

        return False

class PhysicalBoard(Board):
    def __init__(self, columns, rows, X, Y, width, height):
        super().__init__(columns, rows)

        self.X = X
        self.Y = Y
        self.width = width
        self.height = height
        self.PhysicalBoardSquares = []
        self.smallfont = pygame.font.Font("fonts/freesansbold.ttf", 25)
        self.mediumfont = pygame.font.Font("fonts/freesansbold.ttf", 50)
        self.largefont = pygame.font.Font("fonts/freesansbold.ttf", 80)

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

    def draw(self, gameDisplay, color):
        pygame.draw.rect(gameDisplay, color, (self.X, self.Y, self.width, self.height))

    def drawPhysicalBoardSquares(self, gameDisplay, squareColor):
        for pbs in self.PhysicalBoardSquares:
            pbs.draw(gameDisplay, squareColor)

            #draw the position # on the board for usability
            textSurface = self.smallfont.render(str(pbs.position), True, (0,0,0))
            textRect = textSurface.get_rect()
            textRect.center = (pbs.X + 15), (pbs.Y + 15)
            gameDisplay.blit(textSurface, textRect)

            gamePiece = self.GamePieces[pbs.position]
            if gamePiece.type != 'Empty':
                textSurface = self.largefont.render(gamePiece.type, True, gamePiece.color)
                textRect = textSurface.get_rect()

                # draw the piece in the center of the square
                textRect.center = (pbs.X + pbs.width / 2), (pbs.Y + pbs.height / 2)

                gameDisplay.blit(textSurface, textRect)


    def printMe(self):
        for pbs in self.PhysicalBoardSquares:
            print('Position: ' + str(pbs.position) + ' ' + str(pbs.X) + ' ' + str(pbs.Y))

        #so you don't need the exact name of the class... but the intellisense helps...
        for foo in self.PhysicalBoardSquares:
            print('Position: ' + str(foo.position) + ' ' + str(foo.X) + ' ' + str(foo.Y))


class PhysicalBoardSquare:
    def __init__(self, position, X, Y, width, height):

        self.position = position
        self.X = X
        self.Y = Y
        self.width = width
        self.height = height

    def draw(self, gameDisplay, squareColor):
        pygame.draw.rect(gameDisplay, squareColor, (self.X, self.Y, self.width, self.height))



class GamePiece:
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


class Player:
    __metaclass__ = abc.ABCMeta

    def __init__(self, playerNum, gamePiece):
        self.playerNum = playerNum
        self.gamePiece = gamePiece
        self.gamesWon = 0

    @abc.abstractmethod
    def getMove(self, newPosition):
        """Implement a getMove method for each type of Player"""
        return


class HumanPlayer(Player):
    def __init__(self, playerNum, gamePiece):
        super().__init__(playerNum, gamePiece)
        self.type = 'human'

    def getMove(self, newPosition):
        return Move(self.gamePiece, newPosition)


class ComputerPlayer(Player):
    def __init__(self, playerNum, gamePiece, searchDepth, evalFunctionVersion):
        super().__init__(playerNum, gamePiece)
        self.type = 'computer'
        self.searchDepth = searchDepth
        self.evalFunctionVersion = evalFunctionVersion

    def getMove(self, newPosition):
        pass


    def getRandomMove(self, gameBoard):
        lOpenPositions = gameBoard.getOpenPositions()
        numOpenPositions = len(lOpenPositions)

        if numOpenPositions > 0:
            randIndex = random.randint(0, numOpenPositions-1)
            randPosition = lOpenPositions[randIndex]
            return Move(self.gamePiece, randPosition)
        else:
            #can't generate a move with no positions available
            raise ValueError('No open positions for a ComputerPlayer to generate a move to!')


#represents one move of a single piece
class Move:
    def __init__(self, gamePiece, newPosition):
        self.gamePiece = gamePiece
        self.newPosition = newPosition


#represents one player's turn and the number of moves made in that turn
class Turn:
    def __init__(self, turnNum, currentPlayer):
        self.turnNum = turnNum
        self.player = currentPlayer
        self.moves = []
        
#should Game have a physical game board or a game board?
#in the future we'll need to check for winners in virtual boards, so the physical board game calls in the isWinner* functions kind of destroy that
class Game:
    def __init__(self, numColumns, numRows, aiDifficulty=None):
        self.numColumns = numColumns
        self.numRows = numRows
        self.aiDifficulty = aiDifficulty
        self.gameBoard = None
        self.gameState = 'In Progress'
        self.gameWinner = None
        self.Players = []
        self.Turns = []

    def getOpponent(self, player):
        if len(self.Players) != 2:
            raise ValueError('This game doesn''t have 2 players')

        #return the opposite player
        if player.playerNum == 1:
            return self.Players[1]
        elif player.playerNum == 2:
            return self.Players[0]

