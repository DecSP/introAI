import pickle
import chess
import numpy as np
import pandas as pd
from train_model import predict_DF

file = './model.sav'
model,enc=None,None
with open(file,'rb') as f:
    model = pickle.load(f)
file2 = './enc.sav'
with open(file2,'rb') as f:
    enc = pickle.load(f)

pawnEvalWhite = [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ]

pawnEvalBlack = pawnEvalWhite[::-1]

knightEval = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ]

bishopEvalWhite = [
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishopEvalBlack = bishopEvalWhite[::-1]

rookEvalWhite = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
]

rookEvalBlack = rookEvalWhite[::-1]

evalQueen = [
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

kingEvalWhite = [

    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
]

kingEvalBlack = kingEvalWhite[::-1]

def getPieceValue(piece, i, j, first):
    value = 0
    if piece == 'p': 
        value = 10 + pawnEvalBlack[i][j]
    elif piece == 'r': 
        value = 50 + rookEvalBlack[i][j]
    elif piece == 'n': 
        value = 30 + knightEval[i][j]
    elif piece == 'b': 
        value = 30 + bishopEvalBlack[i][j]
    elif piece == 'q': 
        value = 90 + evalQueen[i][j]
    elif piece == 'k':  
        value = 900 + kingEvalBlack[i][j]
    elif piece == 'P': 
        value = -(10 + pawnEvalWhite[i][j])
    elif piece == 'R': 
        value = -(50 + rookEvalWhite[i][j])
    elif piece == 'N': 
        value = -(30 + knightEval[i][j])
    elif piece == 'B': 
        value = -(30 + bishopEvalWhite[i][j])
    elif piece == 'Q': 
        value = -(90 + evalQueen[i][j])
    elif piece == 'K': 
        value = -(900 + kingEvalWhite[i][j])

    if first: 
        return -value
    else: 
        return value

def get_board_features(board):
    board_features = []
    for square in chess.SQUARES:
      board_features.append(str(board.piece_at(square)))
    return board_features


def get_move_features(move):
    from_ = [0]*64
    to_ = [0]*64
    from_[move.from_square] = 1
    to_[move.to_square] = 1
    return from_, to_

def get_possible_moves_data(current_board):
    data = []
    moves = list(current_board.legal_moves)
    for move in moves:
      from_square, to_square = get_move_features(move)
      row = get_board_features(current_board)+ from_square+ to_square
      data.append(row)
    return data,moves


def evalBoardML(board,droprate=0.5,x=100):
    global model,enc
    if model is None or enc is None:
        return None
    data,moves = get_possible_moves_data(board)
    predictions = predict_DF(data,model,enc)
    rmoves=[moves[pred[0]] for pred in predictions[max(int((len(moves)-1)*(1-droprate)),len(moves)-x):]]
    return rmoves


def evaluateBoard(board, first):
    totalEvaluate = 0
    for i in range(8):
        for j in range(8):
            pos=i*8+j
            if board.piece_at(pos) is None: continue
            totalEvaluate = totalEvaluate + getPieceValue(board.piece_at(pos).symbol(), i, j, first)
    return totalEvaluate

bestMove=None
origdepth=3
def minimaxroot(depth, board, maximizing, first,lock):
    global bestMove,origdepth
    origdepth=depth
    bestValue = -9999
    Move = None
    for move in evalBoardML(board):
        board.push(move)
        value = minimax(depth-1, board, -10000, 10000, not maximizing, first)
        board.pop()
        if value >= bestValue:
            bestValue = value
            Move = move

    lock.acquire()
    bestMove=Move
    lock.release()

def minimax(depth, board, alpha, beta, maximizing, first):
    if depth == 0:
        return -evaluateBoard(board, first)
    d=origdepth-depth
    x=100
    if d<3:
        scale=0.7
    else:
        scale=0.8
        x=3
    
    if maximizing:
        bestValue = -9999

        for move in evalBoardML(board,scale,x):
            board.push(move)
            bestValue = max(bestValue, minimax(depth-1, board, alpha, beta, not maximizing, first))
            board.pop()
            alpha = max(alpha, bestValue)
            if (beta <= alpha): 
                return bestValue  
                          
        return bestValue

    else:
        bestValue = 9999

        for move in evalBoardML(board,scale,x):
            board.push(move)
            bestValue = min(bestValue, minimax(depth-1, board, alpha, beta, not maximizing, first))
            board.pop()
            beta = min(beta, bestValue)
            if (beta <= alpha): 
                return bestValue  
                          
        return bestValue