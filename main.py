print('Play First (1) or Second (2)?')
goFirst = input() == '1'

from monteCarloTree import *
from visuals import *
import os

def finishGame(outcome):
    s = ''
    if outcome == -1:
        s = 'Tie!'
    if outcome == 0:
        s = 'Player 1 Wins!'
    if outcome == 1:
        s = 'Player 2 Wins!'
    c = int((120 - len(s)) / 2)
    screen.addstr(3, c, s)
    screen.getch()

def showConfidence(confidence):
    s = ' The tree is ' + str(int(confidence * 10000) / 100) + '% sure it will win. '
    c = int((120 - len(s)) / 2)
    screen.addstr(25, c, s)



screen.border()

board = getBitBoard()
drawBoard(board)

tree = MonteCarloTree(board, 0)

firstTurn = True

while True:
    if goFirst or (not firstTurn):
        move = getConnectFourMove(board)
        board = makeMove(board, 1 - goFirst, move)
        tree.makeMove(move)
        drawBoard(board)

        if (data := checkWin(board))[0]:
            finishGame(data[1])
            break

    firstTurn = False

    for i in range(5000):
        tree.step()

    board = makeMove(board, 0 + goFirst, tree.getBestMove())
    drawBoard(board)
    showConfidence(1 - (tree.root.wins / tree.root.visits))

    if (data := checkWin(board))[0]:
        finishGame(data[1])
        break
