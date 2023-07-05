from connectFour import *
import curses

height, width = 29, 119
boardR, boardC = 5, 43

ENTER = 10
LEFT = 260
RIGHT = 261

screen = curses.initscr()
screen.scrollok(False)
screen.keypad(True)
curses.resize_term(height + 1, width + 1)
curses.curs_set(0)
curses.noecho()


def drawBlackPiece(r, c):
    screen.addstr(r, c, '/‾‾\\')
    screen.addstr(r + 1, c, '\\__/')


def drawWhitePiece(r, c):
    screen.addstr(r, c, '/▒▒\\')
    screen.addstr(r + 1, c, '\\▒▒/')

def drawBoard(board):
    for i in range(7):
        for j in range(6):
            if (board[0] >> (j + i * 7)) % 2:
                drawWhitePiece(boardR + 3 * (5 - j), boardC + 5 * i)
            if (board[1] >> (j + i * 7)) % 2:
                drawBlackPiece(boardR + 3 * (5 - j), boardC + 5 * i)
    for i in range(34):
        screen.addstr(boardR + 17, boardC + i, "─")
    for i in range(34):
        screen.addstr(boardR - 1, boardC + i, "─")


def getConnectFourMove(board):
    legalMoves = getMoves(board)
    pos = 3
    screen.addstr(boardR + 18, boardC + 1 + (pos * 5), '/\\')
    while (move := screen.getch()) != ENTER or pos not in legalMoves:
        screen.addstr(boardR + 18, boardC + 1 + (pos * 5), '  ')
        if move == LEFT:
            pos -= 1
        if move == RIGHT:
            pos += 1
        pos = (pos + 7) % 7
        screen.addstr(boardR + 18, boardC + 1 + (pos * 5), '/\\')
    screen.addstr(boardR + 18, boardC + 1 + (pos * 5), '  ')
    return pos
