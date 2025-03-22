import numpy as np

class boardClass(object):
    def __init__(self, m_boardSize: int | tuple[int, ...], m_numMines: int, dim: int=2):
        if isinstance(m_boardSize, tuple):
            dim = len(m_boardSize)
            self.shape = m_boardSize
        else:
            self.shape = (m_boardSize,) * dim

        if dim > 2:
            raise ValueError(f"Only one or two dimensions supported, got {dim}")
        
        self.dim = dim
        self.numMines = m_numMines
        
        self.values = np.zeros(self.shape, dtype=int)
        self.selected = np.zeros(shape=self.values.shape, dtype=bool)

        mine_indices = np.array(np.unravel_index(np.random.choice(self.values.size, size=m_numMines, replace=False), self.values.shape))
        self.values[*mine_indices] = -1

        for m in range(mine_indices.shape[-1]):
            mine_index = mine_indices[:, m]
            current_index = mine_index.copy()
            for k in range(dim):
                for a in [-1, 0, 1]:
                    if mine_index[k] + a >= self.values.shape[k] or mine_index[k] + a < 0:
                        continue
                    current_index[k] = mine_index[k] + a
                    for j in range(k):
                        for b in [-1, 0, 1]:
                            if mine_index[j] + b >= self.values.shape[j] or mine_index[j] + b < 0:
                                continue
                            current_index[j] = mine_index[j] + b 
                            self.values[*current_index] += 1 if self.values[*current_index] >= 0 else 0


        self.selectableSpots = self.values.size - m_numMines

    @property
    def boardSize(self):
        return self.values.shape[0] # TODO generalize
    
    def __str__(self):
        if self.dim > 2:
            raise ValueError(f"Only one or two dimensions supported, got {self.dim}")
        returnString = " "
        divider = "\n---"

        if len(self.values.shape > 1):

            for i in range(0, self.values.shape[0]):
                returnString += " | " + str(i)
                divider += "----"
            divider += "\n"

        returnString += divider
        for y in range(0, self.boardSize):
            returnString += str(y)
            for x in range(0, self.boardSize):
                if self.values[x, y] < 0 and self.selected[x, y]:
                    returnString += " |" + str(self.values[x, y])
                elif self.selected[x, y]:
                    returnString += " | " + str(self.values[x, y])
                else:
                    returnString += " |  "
            returnString += " |"
            returnString += divider
        return returnString

    def makeMove(self, x, y):
        self.selected[x, y] = True
        self.selectableSpots -= 1
        if self.values[x, y] == -1:
            return False
        if self.values[x, y] == 0:
            for i in range(x-1, x+2):
                if i >= 0 and i < self.boardSize:
                    if y-1 >= 0 and not self.selected[i, y-1]:
                        self.makeMove(i, y-1)
                    if y+1 < self.boardSize and not self.selected[i, y+1]:
                        self.makeMove(i, y+1)
            if x-1 >= 0 and not self.selected[x-1,y]:
                self.makeMove(x-1, y)
            if x+1 < self.boardSize and not self.selected[x+1, y]:
                self.makeMove(x+1, y)
            return True
        else:
            return True

    def hitMine(self, x, y):
        return self.values[x, y] == -1

    def isWinner(self):
        return self.selectableSpots == 0

def increment_tuple(t: tuple, index: int = 0, value: int = 1) -> tuple:
    if not t or index < 0 or index >= len(t):
        return t  # Return original tuple if empty or index is out of range
    
    t_list = list(t)
    t_list[index] += value
    return tuple(t_list)

#play game
def playGame():
    boardSize = int(input("Choose the Width of the board: "))
    numMines = int(input("Choose the number of mines: "))
    dim = int(input("Choose dimensions of board: "))
    gameOver = False
    winner = False
    Board = boardClass(boardSize, numMines, dim=dim)
    while not gameOver:
        print(Board)
        print("Make your move:")
        x = int(input("x: "))
        y = int(input("y: "))
        Board.makeMove(x, y)
        gameOver = Board.hitMine(x, y)
        if Board.isWinner() and gameOver is False:
            gameOver = True
            winner = True

    print(Board)
    if winner:
        print("Congratulations, You Win!")
    else:
        print("You hit a mine, Game Over!")

if __name__ == "__main__":
    playGame()
