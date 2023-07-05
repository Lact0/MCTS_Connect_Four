from connectFour import *
import random
import math

class MonteCarloTree:
    def __init__(this, board, player, c = 2 ** .5, initVisits = 100):
        this.player = player
        this.root = MonteCarloNode(board, player, None)
        this.c = c
        this.initVisits = initVisits

    def step(this):
        node = this.selectLeaf()
        if node.terminal:
            node.backpropogate(node.outcome)
        else:
            node.expand()
            node = node.select(this.c, this.initVisits)[1]
            outcome = node.simulate()
            node.backpropogate(outcome)

    def selectLeaf(this):
        node = this.root
        while node.children is not None:
            node = node.select(this.c, this.initVisits)[1]
        return node

    def getBestMove(this):
        bestMove = this.root.select(0, this.initVisits)[0]
        this.makeMove(bestMove)
        return bestMove

    def makeMove(this, move):
        legalMoves = getMoves(this.root.board)
        if move not in legalMoves:
            return False
        if this.root.children is None:
            this.root.expand()
        this.root = this.root.children[move]
        this.root.parent = None

#Parent is None if it is the root
class MonteCarloNode:
    def __init__(this, board, player, parent):
        this.board = board
        this.player = player
        this.visits = 0
        this.wins = 0
        this.children = None
        this.parent = parent
        this.terminal, this.outcome = checkWin(board)

    def update(this, outcome):
        this.visits += 1
        if outcome == -1:
            this.wins += .5
        if this.player == outcome:
            this.wins += 1

    def select(this, c, initialVisits):
        maxMove, maxVal = 0, -1
        for move in this.children:
            child = this.children[move]
            visits = initialVisits if this.visits == 0 else this.visits
            childVisits = initialVisits if child.visits == 0 else child.visits
            uct = c * ((math.log(visits) / childVisits) ** .5)
            value = (childVisits - child.wins) / childVisits + uct
            if value > maxVal:
                maxMove = move
                maxVal = value
        return (maxMove, this.children[maxMove])

    def expand(this):
        this.children = {}
        moves = getMoves(this.board)
        for move in moves:
            newBoard = makeMove(this.board, this.player, move)
            this.children[move] = MonteCarloNode(newBoard, (this.player + 1) % 2, this)

    def simulate(this):
        board = this.board
        turn = this.player
        while not (data := checkWin(board))[0]:
            move = random.choice(getMoves(board))
            board = makeMove(board, turn, move)
            turn = (turn + 1) % 2
        return data[1]

    def backpropogate(this, outcome):
        if this.parent is None:
            return
        this.update(outcome)
        this.parent.backpropogate(outcome)
