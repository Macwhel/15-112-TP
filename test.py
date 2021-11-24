rows = cols = 5

def pprintBoard(board: list) -> None:
    for row in board:
        print(row)

board = [[0] * cols for _ in range(rows)]

pprintBoard(board)



