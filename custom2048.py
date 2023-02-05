from tkinter import *
from colour import *
import random
import functools

#Square class
class Square(LabelFrame):
    num = 1
    def __init__(self,parent,row,col,value):
        super().__init__(parent, height=32, width=32, font=20,labelanchor='n',relief=FLAT)
        self.row = row
        self.col = col
        self.value = value
        self.place(x=col*40+2,y=row*40+2)
        label = Label(self,foreground='white',font=20, text=str(value))
        label.place(relx=0.5,rely=0.5,anchor=CENTER)
        color(self,label,value)
        self.num = Square.num
        Square.num = Square.num + 1

#global variables
gameStarted = False
squaresList = []
activatedSquaresList = []
initRed = 0
initGreen = 0
initBlue = 0
moving = False

#define box commands
def color(widget1,widget2,value):
    global initRed
    global initGreen
    global initBlue
    if initRed > 0.5:
        r = initRed - 0.02 * value
    else:
        r = initRed + 0.02 * value
    if initGreen > 0.5:
        g = initGreen - 0.02 * value
    else:
        g = initGreen + 0.02 * value
    if initBlue > 0.5:
        b = initBlue - 0.02 * value
    else:
        b = initBlue + 0.02 * value

    if r > 1:
        initRed = random.random()
        r = 0.8
    if g > 1:
        initGreen = random.random()
        g = 0.8
    if b > 1:
        initBlue = random.random()
        b = 0.8
    if r < 0:
        initRed = random.random()
        r = 0.2
    if g < 0:
        initGreen = random.random()
        g = 0.2
    if b < 0:
        initBlue = random.random()
        b = 0.2

    widget1.config(bg=Color(rgb=(r,g,b)))
    widget2.config(bg=Color(rgb=(r, g, b)))

def changeBoard(event):
    global gameStarted
    gameStarted = False
    startButton.config(text="Start")
    resetBoard()

def resetBoard():
    global initRed
    global initGreen
    global initBlue
    initRed = random.random()
    initGreen = random.random()
    initBlue = random.random()
    for row in range(10):
        for col in range(10):
            if squaresList[row][col]["occupied"] != "empty" and squaresList[row][col]["occupied"] != "wall":
                squaresList[row][col]["occupied"].destroy()
                squaresList[row][col]["occupied"] = "empty"
            if  squaresList[row][col]["activated"] == False:
                squaresList[row][col]["square"].config(bg=Color(rgb=(0.6, 0.9, 0.7)))
                squaresList[row][col]["occupied"] = "wall"
            else:
                squaresList[row][col]["occupied"] = "empty"

def startGame(event):
    global gameStarted
    gameStarted = True
    resetBoard()
    for row in range(10):
        for col in range(10):
            if squaresList[row][col]["activated"] == 0:
                squaresList[row][col]["square"].config(bg=Color(rgb=(0.5,0.5,0.5)))

    startButton.config(text="Restart")
    newSquare()
    newSquare()

def newSquare():
    initialValues = [2,2,2,2,2,2,2,2,2,4]
    randomInitialValue = initialValues[random.randint(0,9)]
    row = 0
    col = 0
    while(squaresList[row][col]["occupied"]!="empty"):
        randomNumber = random.randint(0, len(activatedSquaresList) - 1)
        row = int(activatedSquaresList[randomNumber]["square"].winfo_y() / 40)
        col = int(activatedSquaresList[randomNumber]["square"].winfo_x() / 40)
    s = Square(arena,row,col, randomInitialValue)
    #print("New Square " + str(s.num))
    squaresList[row][col]["occupied"] = s
    s.update()

def keyPressed(event,key):
    global moving
    if moving == False:
        moving = True
        global change
        change = False
        print("start moveSquare")
        for r in squaresList:
            for s in r:
                s["combinedAlready"] = False

        if key == "Left":
            horShift = -1
            verShift = 0
            col = 1
            while col < 10:
                row = 0
                while row < 10:
                    moveSquare(row, col, horShift, verShift)

                    row = row + 1
                col = col + 1
        elif key == "Right":
            horShift = 1
            verShift = 0
            col = 8
            while col > -1:
                row = 0
                while row < 10:
                    moveSquare(row, col, horShift, verShift)

                    row = row + 1
                col = col - 1
        elif key == "Up":
            horShift = 0
            verShift = -1
            row = 1
            while row < 10:
                col = 0
                while col < 10:
                    moveSquare(row, col, horShift, verShift)

                    col = col + 1
                row = row + 1
        elif key == "Down":
            horShift = 0
            verShift = 1
            row = 8
            while row > -1:
                col = 0
                while col < 10:
                    moveSquare(row, col, horShift, verShift)

                    col = col + 1
                row = row - 1
        if change:
            newSquare()
        print("end moveSquare")
        moving = False


def moveSquare(row,col,x,y):
    global change
    if squaresList[row][col]["occupied"] != "empty" and squaresList[row][col]["occupied"] != "wall":
        square = squaresList[row][col]["occupied"]
        squareRow = row
        squareCol = col
        while squareRow < 10-y and squareRow > -1-y and squareCol < 10-x and squareCol > -1-x and squaresList[squareRow+y][squareCol+x]["occupied"] != "wall":
            if squaresList[squareRow+y][squareCol+x]["occupied"] != "empty" and squaresList[squareRow+y][squareCol+x][
                "occupied"].value == square.value and squaresList[squareRow+y][squareCol+x]["combinedAlready"] == False:
                for i in range(20):
                    square.place(x=square.winfo_x() - 2 + 2*x, y=square.winfo_y() - 2 + 2*y)
                    square.update()
                #print("Kill Square " + str(squaresList[squareRow+y][squareCol+x]["occupied"].num))
                squaresList[squareRow+y][squareCol+x]["occupied"].destroy()
                squaresList[squareRow+y][squareCol+x]["occupied"] = square
                squaresList[squareRow + y][squareCol + x]["combinedAlready"] = True
                squaresList[squareRow][squareCol]["occupied"] = "empty"
                square.row = square.row + y
                square.col = square.col + x
                square.value = square.value * 2
                square.winfo_children()[0].config(text=square.value)
                color(square,square.winfo_children()[0],square.value)
                squareRow = squareRow + y
                squareCol = squareCol + x
                change = True
                break
            elif squaresList[squareRow+y][squareCol+x]["occupied"] == "empty":
                #print("Move Square " + str(square.num))
                for i in range(20):
                    square.place(x=square.winfo_x() - 2 + 2 * x, y=square.winfo_y() - 2 + 2 * y)
                    square.update()
                squaresList[squareRow+y][squareCol+x]["occupied"] = square
                squaresList[squareRow][squareCol]["occupied"] = "empty"
                square.row = square.row + y
                square.col = square.col + x
                squareRow = squareRow + y
                squareCol = squareCol + x
                change = True
            else:
                break

def activateSquare(*event,r,c):
    global gameStarted
    if gameStarted == False:
        if squaresList[r][c]["activated"]==0:
            squaresList[r][c]["square"].config(bg=Color(rgb=(1, 1, 1)))
            squaresList[r][c]["activated"] = 1
            squaresList[r][c]["occupied"] = "empty"
            activatedSquaresList.append(squaresList[r][c])
        elif squaresList[r][c]["activated"]==1:
            squaresList[r][c]["square"].config(bg=Color(rgb=(0.6, 0.9, 0.7)))
            squaresList[r][c]["activated"] = 0
            squaresList[r][c]["occupied"] = "wall"
            activatedSquaresList.remove(squaresList[r][c])

#set up game board
window=Tk()

window.title('Custom 2048')
window.geometry("900x600+300+100")
window.bind("<Left>",functools.partial(keyPressed,key="Left"))
window.bind("<Right>",functools.partial(keyPressed,key="Right"))
window.bind("<Up>",functools.partial(keyPressed,key="Up"))
window.bind("<Down>",functools.partial(keyPressed,key="Down"))

arena = LabelFrame(window, relief=FLAT, height=400,width=400,bg = Color(rgb=(1,1,1)))
arena.place(x=100,y=100)

scoreLabel = Label(window, text="Score: ", relief=FLAT)
scoreLabel.place(x=600,y=200)

startButton = Button(window, height = 3, width = 10, text = "Start")
startButton.bind("<Button-1>",startGame)
startButton.place(x=650,y=300)

changeBoardButton = Button(window, height = 3, width = 10, text = "Change Board")
changeBoardButton.bind("<Button-1>",changeBoard)
changeBoardButton.place(x=650,y=400)


#fill gameboard
for row in range(10):
    colList = []
    for col in range(10):
        square = LabelFrame(arena,height=40,width=40,relief=RIDGE,bg=Color(rgb=(0.6,0.9,0.7)))
        square.place(x=col * 40-2, y=row * 40-2)
        square.update()

        colList.append({"square":square,"activated":0,"occupied":"wall","combinedAlready":False})

    squaresList.append(colList)

for row in range(10):
    for col in range(10):
        squaresList[row][col]["square"].bind("<Button-1>", functools.partial(activateSquare,r=row,c=col))
        if (col >= 3 and row >= 3 and col <= 6 and row <= 6):
            activateSquare(squaresList[row][col],r=row,c=col)


#run main loop
window.mainloop()