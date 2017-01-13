import pygame
from PyTicTacToe_Classes import *
import colors as c
#import fonts

pygame.init()

white = (255,255,255)
gray = (200,200,200)
green = (0,255,0)
red = (255,0,0)

display_width = 700
display_height = 700
COLUMNS = 3
ROWS = 3
mainGameList = []
mainGame = None

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('PyTicTacToe')

FPS = 10

testBoxX = 400
testBoxY = 300
boxWidth = 40
boxHeight = 40

smallfont = pygame.font.Font("fonts/freesansbold.ttf", 25)
mediumfont = pygame.font.Font("fonts/freesansbold.ttf", 50)
largefont = pygame.font.Font("fonts/freesansbold.ttf", 80)

# panelX = (display_width * 0.1) / 2
# panelWidth = display_width * 0.9
# panelY = (display_height * 0.15) / 2
# panelHeight = display_height * 0.9

#make the board square 6 pixels less than 1/3 the size of the panel so we can fit 3 across and 3 down
#boardSquareSize = int((panelWidth / 3) - 6)

boxSelected = False

def startNewGame():
    global mainGameList
    global mainGame

    panelX = (display_width * 0.1) / 2
    panelWidth = display_width * 0.9
    panelY = (display_height * 0.15) / 2
    panelHeight = display_height * 0.9
    mainGame = Game(COLUMNS, ROWS)
    mainGameList.append(mainGame)
    gamePieceX = GamePiece('X', c.green)
    gamePieceO = GamePiece('O', c.blue)
    player1 = HumanPlayer(1, gamePieceX)
    #player2 = HumanPlayer(2, gamePieceO)
    player2 = ComputerPlayer(2, gamePieceO, 2, 1)
    firstTurn = Turn(len(mainGame.Turns)+1, player1)

    #this draws the gray panel that represents our game board
    #it will mostly be covered by BoardSquares
    mainBoard = PhysicalBoard(COLUMNS, ROWS, panelX, panelY, panelWidth, panelHeight)
    #mainBoard.printMe()

    #add stuff to the game object
    mainGame.gameBoard = mainBoard
    mainGame.Players.append(player1)
    mainGame.Players.append(player2)
    mainGame.Turns.append(firstTurn)

def main():
    #global mainGameList
    global mainGame

    # panelX = (display_width * 0.1) / 2
    # panelWidth = display_width * 0.9
    # panelY = (display_height * 0.15) / 2
    # panelHeight = display_height * 0.9
    #
    # mainGame = Game(COLUMNS, ROWS)
    # mainGameList.append(mainGame)
    # gamePieceX = GamePiece('X', c.green)
    # gamePieceO = GamePiece('O', c.blue)
    # player1 = HumanPlayer(1, gamePieceX)
    # player2 = HumanPlayer(2, gamePieceO)
    # currentTurn = Turn(len(mainGame.Turns)+1, player1)
    #
    # #this draws the gray panel that represents our game board
    # #it will mostly be covered by BoardSquares
    # mainBoard = PhysicalBoard(COLUMNS, ROWS, panelX, panelY, panelWidth, panelHeight)
    # #mainBoard.printMe()
    #
    # #add stuff to the game object
    # mainGame.gameBoard = mainBoard
    # mainGame.Players.append(player1)
    # mainGame.Players.append(player2)
    # mainGame.Turns.append(currentTurn)

    ###############
    startNewGame()
    currentTurn = mainGame.Turns[len(mainGame.Turns)-1]
    mainBoard = mainGame.gameBoard

    global testBoxX
    global testBoxY

    double_click_event = pygame.USEREVENT + 1
    timer = 0
    double_click_duration = 220
    last_click = 0

    mouseDown = False
    double_click = False

    gameOver = False
    gameExit = False


    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #use keys for testing certain functions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print('How big is the game pieces list?')
                    print(str(len(mainBoard.GamePieces)))

                if event.key == pygame.K_w:
                    print('What positions on the board are empty?')
                    print(mainBoard.getOpenPositions())

                if event.key == pygame.K_e:
                    print('PhysicalBoardSquares')
                    mainBoard.printMe()

                if event.key == pygame.K_r:
                    #check all 3 winners from left to right
                    print('Checking winners to the right...')
                    for i in range(0, mainBoard.numColumns * mainBoard.numRows):
                        print('Is position ' + str(i) + ' a winner?: ' + str(mainBoard.isWinnerToTheRight(i)))

                if event.key == pygame.K_t:
                    #check all 3 winners from top to bottom
                    print('Checking winners from top to bottom...')
                    for i in range(0, mainBoard.numColumns * mainBoard.numRows):
                        print('Is position ' + str(i) + ' a winner?: ' + str(mainBoard.isWinnerFromTopToBottom(i)))

                if event.key == pygame.K_y:
                    #check winner diagonally down and to the right
                    print('Checking winner diagonally down and to the right and up to the right...')
                    for i in range(0, mainBoard.numColumns * mainBoard.numRows):
                        print('Is position ' + str(i) + ' a winner down to right?: ' + str(mainBoard.isWinnerDiagonallyDownToRight(i)))
                        print('Is position ' + str(i) + ' a winner up to right?:   ' + str(mainBoard.isWinnerDiagonallyUpToRight(i)))

                if event.key == pygame.K_u:
                    #check winners of all positions
                    print('Checking winners of ALL positions...')
                    for i in range(0, mainBoard.numColumns * mainBoard.numRows):
                        print('Is position ' + str(i) + ' a winner?: ' + str(mainBoard.isWinnerAtPosition(i)))

                if event.key == pygame.K_i:
                    #restart the game
                    if gameOver:
                        gameOver = False
                        startNewGame()
                        currentTurn = mainGame.Turns[len(mainGame.Turns) - 1]
                        mainBoard = mainGame.gameBoard


            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.button)
                if event.button == 1:
                    mouseDown = True

                    now = pygame.time.get_ticks()
                    if (now - last_click) <= double_click_duration:
                        #print('double click ' + str(now) + ' ' + str(last_click) + ' Diff:' + str((now - last_click)))
                        double_click = True
                    else:
                        pass
                        #print('single click ' + str(now) + ' ' + str(last_click) + ' Diff:' + str((now - last_click)))

                    last_click = pygame.time.get_ticks()

            if event.type == pygame.MOUSEBUTTONUP:
                #print(event.button)
                #this gets the amount of x,y movement of the mouse since the last call of the function
                #therefore i'm calling the function and doing nothing with it the moment i press the button down
                #print(pygame.mouse.get_rel())
                #print(pygame.mouse.get_pos())

                if event.button == 1:
                    mouseDown = False

        gameDisplay.fill(white)

        #reprint the box every frame the mouse is being held down
        #even at 60 FPS this is tough to keep the cursor on the box
        #drag_n_drop(mouseDown)

        #attach the box to the mouse cursor if we click over the box
        #attach_box_to_cursor(mouseDown)

        #if the current game has ended just keep looping until the player quits or clicks the new game button
        if gameOver:
            double_click = False
            drawText('Do you want to play again?  Press i', 300, 100)

            p1Wins, p2Wins = countWinners()
            drawText('Player 1 has won ' + str(p1Wins) + ' games!', 300, 200)
            drawText('Player 2 has won ' + str(p2Wins) + ' games!', 300, 300)

            pygame.display.update()
            continue

        if currentTurn.player.type == 'human':
            # if we have double clicked let's determine what PhysicalBoardSquare was clicked on
            if double_click:
                positionClicked = getPositionClicked(mainBoard)

                if positionClicked != -1:
                    weMoved = handleDoubleClick(mainBoard, currentTurn, positionClicked)

                    print('currentTurn #: ' + str(currentTurn.turnNum) + ' Player: ' + str(currentTurn.player.playerNum))

                    #if we made a move
                    if weMoved:
                        #is the game over?
                        if mainBoard.isThereAWinner():
                            gameOver = True
                            print('Game over!  The winner is HumanPlayer ' + str(currentTurn.player.playerNum) + ' with the move at position ' + str(positionClicked) + '!')
                            mainGame.gameWinner = currentTurn.player
                            mainGame.gameState = 0
                        else:
                            newTurn = Turn(currentTurn.turnNum + 1, mainGame.getOpponent(currentTurn.player))
                            mainGame.Turns.append(newTurn)
                            #currentTurn = None
                            currentTurn = newTurn
                            print('newTurn #: ' + str(newTurn.turnNum) + ' Player: ' + str(currentTurn.player.playerNum))
                            #mainBoard.printMe()
                            #print(str(mainBoard.getPieceAtPosition(6).type))

                    double_click = False
                    #mainBoard.printMe()
        elif currentTurn.player.type == 'computer':
            #the computer needs to search for a move
            move = currentTurn.player.getRandomMove(mainBoard)
            currentTurn.moves.append(move)
            mainBoard.GamePieces[move.newPosition] = move.gamePiece

            if mainBoard.isThereAWinner():
                gameOver = True
                print('Game over!  The winner is ComputerPlayer ' + str(
                    currentTurn.player.playerNum) + ' with the move at position ' + str(positionClicked) + '!')
                mainGame.gameWinner = currentTurn.player
                mainGame.gameState = 0
            else:
                newTurn = Turn(currentTurn.turnNum + 1, mainGame.getOpponent(currentTurn.player))
                mainGame.Turns.append(newTurn)
                currentTurn = newTurn

        #at the end of the loop draw the board, display it and tick the clock
        mainBoard.draw(gameDisplay, c.gray)
        mainBoard.drawPhysicalBoardSquares(gameDisplay, c.red)

        pygame.display.update()
        clock.tick(FPS)



def getPositionClicked(gameBoard):
    positionClicked = -1
    pos = pygame.mouse.get_pos()

    mouseX = pos[0]
    mouseY = pos[1]

    for pbs in gameBoard.getPhysicalBoardSquares:
        if pbs.X <= mouseX <= (pbs.X + pbs.width) and pbs.Y <= mouseY <= (pbs.Y + pbs.height):
            positionClicked = pbs.position
            print('This square was double clicked: ' + str(positionClicked))

    return positionClicked

def handleDoubleClick(gameBoard, currentTurn, positionClicked):
    # if this square is empty, then place the piece of the current player into the square
    if gameBoard.GamePieces[positionClicked].type == 'Empty':
        move = currentTurn.player.getMove(positionClicked)
        currentTurn.moves.append(move)
        gameBoard.GamePieces[positionClicked] = move.gamePiece

        #since we found a non-empty space and placed a piece, end this turn
        return True

    return False

def drawText(text, x, y):
    textSurface = smallfont.render(text, True, c.blue)
    textRect = textSurface.get_rect()
    textRect.center = x, y
    gameDisplay.blit(textSurface, textRect)

def countWinners():
    p1Wins = 0
    p2Wins = 0

    for game in mainGameList:
        if game.gameWinner.playerNum == 1:
            p1Wins += 1
        elif game.gameWinner.playerNum == 2:
            p2Wins += 1

    return p1Wins, p2Wins



#deprecated
def drag_n_drop(mouseDown):
    global testBoxX
    global testBoxY
    ########################################################

    # track where the mouse is while button 1 is held down
    # and print a green box that follows the mouse
    if mouseDown:
        pos = pygame.mouse.get_pos()

        mouseX = pos[0]
        mouseY = pos[1]
        # print('Mouse is at: ' + str(pos))

        # check if the mouse click is within the boundaries of our box
        if testBoxX <= mouseX <= (testBoxX + boxWidth) and testBoxY <= mouseY <= (testBoxY + boxHeight):
            print('mouse click in XY bounds of box')
            # print(pos[0])
            testBoxX = mouseX - (boxWidth / 2)
            testBoxY = mouseY - (boxHeight / 2)

    pygame.draw.rect(gameDisplay, green, (testBoxX, testBoxY, boxWidth, boxHeight))

    # else:
    #     #only draw this rectangle when the mouse isn't pressed
    #     pygame.draw.rect(gameDisplay, green, (testBoxX, testBoxY, boxWidth, boxHeight))

    # print('framezzzzzzzz')
    ########################################################

#probably deprecated
def attach_box_to_cursor(mouseDown):
    global testBoxX
    global testBoxY
    global boxSelected

    pos = pygame.mouse.get_pos()

    mouseX = pos[0]
    mouseY = pos[1]

    if boxSelected == False:
        #if the mouse is within the bounds of the box, then make boxSelected = True and attach it to the cursor
        if mouseDown:
            # print('Mouse is at: ' + str(pos))
            # check if the mouse click is within the boundaries of our box
            if testBoxX <= mouseX <= (testBoxX + boxWidth) and testBoxY <= mouseY <= (testBoxY + boxHeight):
                #print('mouse click in XY bounds of box')
                boxSelected = True
    else:
        if mouseDown:
            if testBoxX <= mouseX <= (testBoxX + boxWidth) and testBoxY <= mouseY <= (testBoxY + boxHeight):
                # if we just clicked earlier and have been dragging the box around, drop it down
                    boxSelected = False

        #if boxSelected = True then draw the box to follow the mouse cursor
        testBoxX = mouseX - (boxWidth / 2)
        testBoxY = mouseY - (boxHeight / 2)

    pygame.draw.rect(gameDisplay, green, (testBoxX, testBoxY, boxWidth, boxHeight))



if __name__ == '__main__':
    main()