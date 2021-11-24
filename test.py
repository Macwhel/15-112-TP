import random

rows = cols = 10

def pprintBoard(board: list) -> None:
    for row in board:
        print(row)

# init board
board = [[0] * cols for _ in range(rows)]

# init locations of all cells


pprintBoard(board)

# get a random cell
# connect it with another cell

r, c = random.randrange(rows), random.randrange(cols)




