def getBitBoard():
    return (0, 0)


def getMask(board):
    return board[0] | board[1]


def checkPlayerWin(board, player):
    pos = board[player]
    m = pos & (pos >> 7)
    if m & (m >> 14):
        return True

    m = pos & (pos >> 6)
    if m & (m >> 12):
        return True

    m = pos & (pos >> 8)
    if m & (m >> 16):
        return True

    m = pos & (pos >> 1)
    if m & (m >> 2):
        return True

    return False


def checkWin(board):
    player1 = checkPlayerWin(board, 0)
    player2 = checkPlayerWin(board, 1)
    if player1:
        return (True, 0)
    if player2:
        return (True, 1)
    if len(getMoves(board)) == 0:
        return (True, -1)
    return (False, None)


def getMoves(board):
    mask = getMask(board)
    moves = []
    for i in range(7):
        if not (mask >> (5 + 7 * i)) % 2:
            moves.append(i)
    return tuple(moves)


def makeMove(board, player, move):
    newBoard = [board[0], board[1]]
    mask = getMask(board)
    newMask = mask | (mask + (1 << (move * 7)))
    newBoard[player] = board[(player + 1) % 2] ^ newMask
    return (newBoard[0], newBoard[1])
