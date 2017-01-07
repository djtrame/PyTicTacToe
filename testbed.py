import pygame

pygame.init()

white = (255,255,255)
gray = (200,200,200)
green = (0,255,0)
red = (255,0,0)

display_width = 700
display_height = 700

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('testbed')

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

smallfont = pygame.font.Font("fonts/freesansbold.ttf", 25)
mediumfont = pygame.font.Font("fonts/freesansbold.ttf", 50)
largefont = pygame.font.Font("fonts/freesansbold.ttf", 80)

def main():
    global testBoxX
    global testBoxY



    mouseDown = False


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.button)
                if event.button == 1:
                    mouseDown = True

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
        attach_box_to_cursor(mouseDown)

        draw_panel()

        draw_boxes()

        pygame.display.update()
        clock.tick(FPS)

def draw_boxes():
    #draw 9 boxes to simulate a tictactoe board
    # pygame.draw.rect(gameDisplay, red, (panelX, panelY, boardSquareSize, boardSquareSize))

    #figure out a way to draw 3 across and 3 down
    rows = 3
    columns = 3

    #add 2 pixels to a proportion of the panel width
    proportionedPanelSize = int(panelWidth / columns)+2

    boardSquareX = panelX
    boardSquareY = panelY

    #loop through the columns from left to right
    for i in range(0,columns):
        #adjust the top left X coordinate point of each board square
        boardSquareX = panelX + (proportionedPanelSize * i)

        #loop through the rows from top to bottom
        for j in range(0,rows):
            #adjust the top left Y coordinate of each board square
            boardSquareY = panelY + (proportionedPanelSize * j)
            pygame.draw.rect(gameDisplay, red, (boardSquareX, boardSquareY, boardSquareSize, boardSquareSize))



def draw_panel():
    # draw a game panel in the middle of the screen
    # use the last 10% of the screen width and divide it by 2 to center the panel

    pygame.draw.rect(gameDisplay, gray, (panelX, panelY, panelWidth, panelHeight))
    # print(panelWidth, panelHeight)

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