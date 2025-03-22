import random
import eel

from minesweeper import boardClass


class GUIBoardClass(boardClass):
    def __str__(self):
        returnString = ""
        for y in range(0, self.boardSize):
            # returnString += str(y)
            for x in range(0, self.boardSize):
                if self.values[x, y] == -1 and self.selected[x, y]:
                    returnString += 'B'

                    # returnString += str(self.board[x][y].value)
                elif self.selected[x, y]:
                    returnString += str(self.values[x, y])
                else:  # empthy cell
                    returnString += "E"
        return returnString


#### For UI ####
eel.init('.//UI')  # path of the webpage folder

GO_IN = False
GAME_OVER = False
WINNER = False
BOARD = ""


@eel.expose
def clickedOnTheCell(x, y):
    global GO_IN
    global GAME_OVER, WINNER
    GO_IN = not GO_IN
    if GO_IN:
        BOARD.makeMove(x, y)
        GAME_OVER = BOARD.hitMine(x, y)
        if BOARD.isWinner() and GAME_OVER == False:
            GAME_OVER = True
            WINNER = True
            print("Won")
        if GAME_OVER and not WINNER:
            print("Game Over")
        GO_IN = not GO_IN
        # print(BOARD)  # return board to js
        return str(BOARD)


@eel.expose
def makeBoard(boardSize, numMines):
    global BOARD
    del BOARD
    BOARD = GUIBoardClass(boardSize, numMines)


web_app_options = {
    "mode": "chrome",
    "port": 8080,
    'chromeFlags': ["--start-fullscreen"]
}

eel.start('index.html', options=web_app_options, suppress_error=True)
