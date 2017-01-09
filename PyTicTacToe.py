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

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('PyTicTacToe')

FPS = 10

testBoxX = 400
testBoxY = 300
boxWidth = 40
boxHeight = 40

panelX = (display_width * 0.1) / 2
panelWidth = display_width * 0.9
panelY = (display_height * 0.15) / 2
panelHeight = display_height * 0.9

#make the board square 6 pixels less than 1/3 the size of the panel so we can fit 3 across and 3 down
boardSquareSize = int((panelWidth / 3) - 6)

boxSelected = False



def main():
    panelX = (display_width * 0.1) / 2
    panelWidth = display_width * 0.9
    panelY = (display_height * 0.15) / 2
    panelHeight = display_height * 0.9

    firstGame = Game(COLUMNS, ROWS)
    gamePieceX = GamePiece('X', c.green)
    gamePieceO = GamePiece('O', c.blue)
    player1 = Player('Human', 1, gamePieceX)
    player2 = Player('Human', 2, gamePieceO)
    currentTurn = Turn(len(firstGame.Turns)+1, player1)

    #this draws the gray panel that represents our game board
    #it will mostly be covered by BoardSquares
    mainBoard = PhysicalBoard(COLUMNS, ROWS, panelX, panelY, panelWidth, panelHeight)
    #mainBoard.printMe()

    #add stuff to the game object
    firstGame.gameBoard = mainBoard
    firstGame.Players.append(player1)
    firstGame.Players.append(player2)
    firstGame.Turns.append(currentTurn)

    global testBoxX
    global testBoxY

    double_click_event = pygame.USEREVENT + 1
    timer = 0
    double_click_duration = 220
    last_click = 0

    mouseDown = False
    double_click = False


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #use keys for testing certain functions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    #check all 3 winners from top to bottom
                    print('Checking winners from top to bottom...')
                    for i in range(0,3):
                        print('Is position ' + str(i) + ' a winner?: ' + str(firstGame.isWinnerFromTopToBottom(i)))

                if event.key == pygame.K_q:
                    #print(str(len(mainBoard.BoardSquares)))
                    print(str(len(mainBoard.GamePieces)))
                if event.key == pygame.K_r:
                    #check all 3 winners from left to right
                    print('Checking winners to the right...')
                    for i in range(0,7,3):
                        print('Is position ' + str(i) + ' a winner?: ' + str(firstGame.isWinnerToTheright(i)))

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

        #if we have double clicked let's determine what PhysicalBoardSquare was clicked on
        if double_click:
            #draw_letter()
            endTurn = handleDoubleClick(mainBoard, currentTurn)
            #print(endTurn)

            print('currentTurn #: ' + str(currentTurn.turnNum) + ' Player: ' + str(currentTurn.player.playerNum))

            #if we end the turn, then generate a new turn and switch the player
            if endTurn:
                newTurn = Turn(currentTurn.turnNum+1, firstGame.getOpponent(currentTurn.player))
                firstGame.Turns.append(newTurn)
                #currentTurn = None
                currentTurn = newTurn
                print('newTurn #: ' + str(newTurn.turnNum) + ' Player: ' + str(currentTurn.player.playerNum))
                #mainBoard.printMe()
                #print(str(mainBoard.getPieceAtPosition(6).type))

            double_click = False
            #mainBoard.printMe()

        mainBoard.draw(gameDisplay, c.gray)
        mainBoard.drawPhysicalBoardSquares(gameDisplay, c.red)


        pygame.display.update()
        clock.tick(FPS)

def handleDoubleClick(gameBoard, currentTurn):
    pos = pygame.mouse.get_pos()

    mouseX = pos[0]
    mouseY = pos[1]

    for PhysicalBoardSquare in gameBoard.getPhysicalBoardSquares:
        if PhysicalBoardSquare.X <= mouseX <= (PhysicalBoardSquare.X + PhysicalBoardSquare.width) and \
            PhysicalBoardSquare.Y <= mouseY <= (PhysicalBoardSquare.Y + PhysicalBoardSquare.height):
            positionClicked = PhysicalBoardSquare.position
            print('This square was double clicked: ' + str(positionClicked))
            # if this square is empty, then place the piece of the current player into the square
            if gameBoard.GamePieces[positionClicked].type == 'Empty':
                newGamePiece = GamePiece(currentTurn.player.gamePiece.type, currentTurn.player.gamePiece.color)
                gameBoard.GamePieces[positionClicked] = newGamePiece
                currentTurn.moves.append(Move(newGamePiece, positionClicked))
                #since we found a non-empty space and placed a piece, end this turn
                return True

            # if PhysicalBoardSquare.gamePiece is None:
            #     PhysicalBoardSquare.gamePiece = GamePiece(currentTurn.player.gamePiece.type, currentTurn.player.gamePiece.color)
            #     currentTurn.moves.append(Move(PhysicalBoardSquare.gamePiece, PhysicalBoardSquare.position))
            #     #since we found a non-empty space and placed a piece, end this turn
            #     return True

    return False



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