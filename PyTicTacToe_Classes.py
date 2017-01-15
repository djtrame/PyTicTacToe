import pygame
import abc
import random
import copy
#from fonts import *

class Board:
    def __init__(self, columns, rows):
        self.numColumns = columns
        self.numRows = rows
        self.BoardSquares = []
        self.GamePieces = []
        self.winningPiece = None

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

    def getPieceAtPoint(self, row, column):
        return self.getPieceAtPosition(self.getPositionFromPoint((row,column)))


    def getIsPointInBounds(self, point):
        x = point[0]
        y = point[1]

        if x < 0 or x >= self.numRows or y < 0 or y >= self.numColumns:
            return False

        return True

    def makeMove(self, move):
        if self.getIsPositionOccupied(move.newPosition):
            raise ValueError('Can''t move here as position ' + str(move.newPosition) + ' is already occupied!')

        self.GamePieces[move.newPosition] = move.gamePiece

    #Boards need to be able to clone themselves because deepcopy wouldn't allow Fonts
    #and copy still retained too many references to the original game board
    def clone(self):
        newBoard = Board(self.numColumns, self.numRows)

        for i in range(0, len(self.GamePieces)):
            newBoard.GamePieces[i] = GamePiece(self.GamePieces[i].type, self.GamePieces[i].color)

        return newBoard


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
                self.winningPiece = self.getPieceAtPosition(i)
                return True

        return False

    def isThereADraw(self):
        #is the board has a winner there is no draw
        if self.isThereAWinner():
            return False

        #if there are any open positions then there isn't a draw
        if len(self.getOpenPositions()) > 0:
            return False
        else:
            return True

    #pycharm thinks this could be a static method because i don't reference self anywhere in the method
    def getOpponentPiece(self, gamePiece):
        if gamePiece.type == 'X':
            return GamePiece('O')
        elif gamePiece.type == 'O':
            return GamePiece('X')


class PhysicalBoard(Board):
    def __init__(self, columns, rows, X, Y, width, height):
        super().__init__(columns, rows)

        self.X = X
        self.Y = Y
        self.width = width
        self.height = height
        self.PhysicalBoardSquares = []
        self.smallFont = pygame.font.Font("fonts/freesansbold.ttf", 25)
        self.mediumFont = pygame.font.Font("fonts/freesansbold.ttf", 50)
        self.largeFont = pygame.font.Font("fonts/freesansbold.ttf", 80)

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
            textSurface = self.smallFont.render(str(pbs.position), True, (0,0,0))
            textRect = textSurface.get_rect()
            textRect.center = (pbs.X + 15), (pbs.Y + 15)
            gameDisplay.blit(textSurface, textRect)

            gamePiece = self.GamePieces[pbs.position]
            if gamePiece.type != 'Empty':
                textSurface = self.largeFont.render(gamePiece.type, True, gamePiece.color)
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


#using abc we want the Player to be inherited by HumanPlayer and ComputerPlayer
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

    def getMove(self, gameBoard):
        #if someone would be so cruel as to give a CPU no ability to look ahead, just go rando
        if self.searchDepth == 0:
            return self.getRandomMove(gameBoard)

        #newBoard = copy.copy(gameBoard)
        newBoard = gameBoard.clone()

        if len(newBoard.getOpenPositions()) == 9:
            return self.getRandomMove(gameBoard)
        else:
            rootNode = MaxNode(gameBoard, None, None)
            rootNode.gamePiece = self.gamePiece
            #rootNode.Evaluator = Evaluator(1, rootNode.MAXVALUE, rootNode.MINVALUE)
            #rootNode.staticEvaluator = Evaluator(1, rootNode.MAXVALUE, rootNode.MINVALUE)
            rootNode.findBestMove(self.searchDepth)

            newMove = rootNode.bestMoveNode.move

            return newMove

    def getRandomMove(self, gameBoard):
        lOpenPositions = gameBoard.getOpenPositions()
        numOpenPositions = len(lOpenPositions)

        if numOpenPositions > 0:
            randIndex = random.randint(0, numOpenPositions-1)
            randPosition = lOpenPositions[randIndex]
            return Move(self.gamePiece, randPosition)
        else:
            #can't generate a move with no positions available
            raise ValueError('No open positions for a ComputerPlayer to generate a random move to!')


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

        
#represents 1 game between 2 players and captures who won when it finishes
class Game:
    def __init__(self, numColumns, numRows, aiDifficulty=None):
        self.numColumns = numColumns
        self.numRows = numRows
        self.aiDifficulty = aiDifficulty
        self.gameBoard = None
        self.gameState = 1 #1=In Progress; 0=Finished
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


class Node:
    __metaclass__ = abc.ABCMeta

    MAXVALUE = 1000
    MINVALUE = -1000
    #staticEvaluator = None

    def __init__(self, gameBoard, parentNode, move, evaluationFunctionVersion):
        self.gameBoard = gameBoard
        self.parentNode = parentNode
        self.move = move
        #self.searchDepth = searchDepth
        self.evaluationFunctionVersion = evaluationFunctionVersion
        self.Evaluator = Evaluator(evaluationFunctionVersion, self.MAXVALUE, self.MINVALUE)

        self.children = []
        self.value = None
        self.bestMoveNode = None
        self.isWinningNode = False
        self.name = 'root'

        #if we have a parent, then our game piece is opposite of theirs
        if self.parentNode is not None:
            self.gamePiece = self.gameBoard.getOpponentPiece(parentNode.gamePiece)
            self.opponentGamePiece = self.gameBoard.getOpponentPiece(self.gamePiece)


    @abc.abstractmethod
    def evaluate(self):
        """Implement an evaluate method for each type of Node"""
        return

    @abc.abstractmethod
    def generateChildren(self):
        """Implement a generateChildren method for each type of Node"""
        return

    @abc.abstractmethod
    def sortChildren(self, unSortedChildren):
        """Implement a sortChildren method for each type of Node"""
        return

    def selectBestMove(self):
        if len(self.children) == 0:
            return

        # code so this randomizes between children with tied value scores
        sortedChildren = self.sortChildren(self.children)

        self.bestMoveNode = sortedChildren[0]
        self.value = self.bestMoveNode.value

    def evaluateChildren(self):
        for node in self.children:
            node.evaluate()

    def isGameEndingNode(self):
        return self.value == self.MAXVALUE or self.value == self.MINVALUE

    def findBestMove(self, depth):
        if depth > 0:
            print('Type: ' + str(type(self)) + ' Piece: ' + self.gamePiece.type + ' Depth: ' + str(depth))
            self.generateChildren()
            self.evaluateChildren()

            winningChildren = [x for x in self.children if x.isGameEndingNode()]

            if len(winningChildren) > 0:
                self.selectBestMove()
                return
            else:
                for node in self.children:
                    node.findBestMove(depth - 1)

                self.selectBestMove()


class MaxNode(Node):
    def __init__(self, gameBoard, parentNode, move, evaluationFunctionVersion=1):
        super().__init__(gameBoard, parentNode, move, evaluationFunctionVersion)

    def generateChildren(self):
        openPositions = self.gameBoard.getOpenPositions()

        for i in range(0, len(openPositions)):
            #newBoard = copy.copy(self.gameBoard)
            newBoard = self.gameBoard.clone()
            newMove = Move(self.gamePiece, openPositions[i])
            newBoard.makeMove(newMove)

            self.children.append(MinNode(newBoard, self, newMove))

    def evaluate(self):
        #print (str(type(self)) + ' evaluating!')
        self.value = self.Evaluator.evaluate(self.gameBoard, self.gamePiece)

    def isWinningNode(self):
        #a max node has won if it's value is the maximum value
        return self.value == self.MAXVALUE

    def sortChildren(self, unSortedChildren):
        sortedChildren = sorted(unSortedChildren, key=lambda node: node.value, reverse=True)
        return sortedChildren

class MinNode(Node):
    def __init__(self, gameBoard, parentNode, move, evaluationFunctionVersion=1):
        super().__init__(gameBoard, parentNode, move, evaluationFunctionVersion)

    def generateChildren(self):
        openPositions = self.gameBoard.getOpenPositions()

        for i in range(0, len(openPositions)):
            #newBoard = copy.copy(self.gameBoard)
            newBoard = self.gameBoard.clone()
            newMove = Move(self.gamePiece, openPositions[i])
            newBoard.makeMove(newMove)

            self.children.append(MaxNode(newBoard, self, newMove))

    def evaluate(self):
        #print (str(type(self)) + ' evaluating!')
        self.value = self.Evaluator.evaluate(self.gameBoard, self.opponentGamePiece)

    def isWinningNode(self):
        #a max node has won if it's value is the maximum value
        return self.value == self.MAXVALUE

    def sortChildren(self, unSortedChildren):
        sortedChildren = sorted(unSortedChildren, key=lambda node: node.value)
        return sortedChildren


class Evaluator:
    def __init__(self, evaluationFunctionVersion, MAXVALUE, MINVALUE):
        self.version = evaluationFunctionVersion
        self.MAXVALUE = MAXVALUE
        self.MINVALUE = MINVALUE

    def evaluate(self, gameBoard, gamePiece):
        if gameBoard.isThereAWinner():
            #print('evaluator found a winner!')
            if gameBoard.winningPiece.type == gamePiece.type:
                return self.MAXVALUE
            else:
                return self.MINVALUE

        #by the time the first one of these runs "gamePiece" is an X when it needs to be an O
        maxNodeValue = self.evaluatePiece(gameBoard, gamePiece)
        minNodeValue = self.evaluatePiece(gameBoard, gameBoard.getOpponentPiece(gamePiece))
        print('    gamePiece: ' + str(gamePiece.type) + ' MaxValue: ' + str(maxNodeValue) + ' MinValue: ' + str(minNodeValue))

        return maxNodeValue - minNodeValue

    def evaluatePiece(self, gameBoard, gamePiece):
        return self.evaluateRows(gameBoard, gamePiece) + self.evaluateColumns(gameBoard, gamePiece) + self.evaluateDiagonals(gameBoard, gamePiece)

    def evaluateRows(self, gameBoard, gamePiece):
        numColumns = gameBoard.numColumns
        numRows = gameBoard.numRows

        score = 0

        #check the rows
        for i in range(0, numRows):
            pieceCount = 0
            rowClean = True

            #check the columns
            for j in range(0, numColumns):
                boardPiece = gameBoard.getPieceAtPoint(i, j)

                if boardPiece.type == gamePiece.type:
                    pieceCount += 1
                elif boardPiece.type == gameBoard.getOpponentPiece(gamePiece).type:
                    rowClean = False
                    break

            if rowClean and pieceCount != 0:
                score += pieceCount

        #print('holy moly score bore')
        return score

    def evaluateColumns(self, gameBoard, gamePiece):
        numColumns = gameBoard.numColumns
        numRows = gameBoard.numRows

        score = 0

        #check the columns
        for j in range(0, numColumns):
            pieceCount = 0
            colClean = True

            #check the rows
            for i in range(0, numRows):
                boardPiece = gameBoard.getPieceAtPoint(i, j)
                #boardPiece = gameBoard.getPieceAtPoint(j, i)

                if boardPiece.type == gamePiece.type:
                    pieceCount += 1
                elif boardPiece.type == gameBoard.getOpponentPiece(gamePiece).type:
                    colClean = False
                    break

            if colClean and pieceCount != 0:
                score += pieceCount

        return score

    def evaluateDiagonals(self, gameBoard, gamePiece):
        pieceCount = 0
        score = 0
        diagonalClean = True
        opponentPiece = gameBoard.getOpponentPiece(gamePiece)

        #handle the down to right diagonal first
        for i in range(0, gameBoard.numColumns):
            boardPiece = gameBoard.getPieceAtPoint(i, i)

            if boardPiece.type == gamePiece.type:
                pieceCount += 1

            if boardPiece.type == opponentPiece.type:
                diagonalClean = False
                break

        if diagonalClean and pieceCount > 0:
            score += pieceCount

        #now handle the down to left diagonal
        row = 0
        col = 2
        pieceCount = 0
        diagonalClean = True

        while row < gameBoard.numRows and col >= 0:
            boardPiece = gameBoard.getPieceAtPoint(row, col)

            if boardPiece.type == gamePiece.type:
                pieceCount += 1

            if boardPiece.type == opponentPiece.type:
                diagonalClean = False
                break

            row += 1
            col -= 1

        if diagonalClean and pieceCount > 0:
            score += pieceCount

        return score

