import pickle
import random
import chess
import numpy as np
import pandas as pd
# from train_model import predict_DF

file = './model.sav'
model,enc=None,None
with open(file,'rb') as f:
    model = pickle.load(f)

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
    from_ = np.zeros(64)
    to_ = np.zeros(64)
    from_[move.from_square] = 1
    to_[move.to_square] = 1
    return from_, to_

def get_possible_moves_data(current_board):
    data = []
    moves = list(current_board.legal_moves)
    for move in moves:
      from_square, to_square = get_move_features(move)
      row = np.concatenate((get_board_features(current_board), from_square, to_square))
      data.append(row)
    
    board_feature_names = chess.SQUARE_NAMES
    move_from_feature_names = ['from_' + square for square in chess.SQUARE_NAMES]
    move_to_feature_names = ['to_' + square for square in chess.SQUARE_NAMES]
    
    columns = board_feature_names + move_from_feature_names + move_to_feature_names
    
    df = pd.DataFrame(data = data, columns = columns)

    for column in move_from_feature_names:
      df[column] = df[column].astype(float)
    for column in move_to_feature_names:
      df[column] = df[column].astype(float)
    return df,moves

def predict_DF(df,model):
    for i in range(64):
        oldV=['None']
        newV=[0]
        for k in chess.PIECE_SYMBOLS[1:]:
            v=getPieceValue(k,i//8,i%8,True)
            oldV+=[k,k.upper()]
            newV+=[v,-v]
        df.iloc[:,i].replace(oldV,newV,inplace=True)
    gotIdx=[i for i in range(df.shape[0])]
    gotPred=list(model.predict_proba(df))
    nl = [[gotIdx[i],gotPred[i][0]] for i in range(len(gotIdx))]
    nl.sort(key=lambda x: -x[1])
    return nl

def evalBoardML(board,droprate=0.5,x=100):
    global model
    data,moves = get_possible_moves_data(board)
    if model is None or data.shape[0]==0:
        return board.legal_moves
    predictions = predict_DF(data,model)
    rmoves=[moves[pred[0]] for pred in predictions[max(int((len(moves)-1)*(1-droprate)),len(moves)-x):]][::-1]
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
def minimaxroot(depth, board, maximizing, first):
    global bestMove,origdepth
    origdepth=depth
    bestValue = -9999
    Move = None
    tmp=evalBoardML(board)
    if len(tmp)>10: depth=3
    else: depth=5
    for move in tmp:
        board.push(move)
        value = minimax(depth-1, board, -10000, 10000, not maximizing, first)
        board.pop()
        if value >= bestValue:
            bestValue = value
            Move = move

    bestMove=Move

def minimax(depth, board, alpha, beta, maximizing, first):
    if depth == 0:
        return -evaluateBoard(board, first)
    elif depth>2:
        legal_moves=evalBoardML(board)
    else:
        legal_moves=list(board.legal_moves)
    
    if maximizing:
        bestValue = -9999

        for move in legal_moves:
            board.push(move)
            bestValue = max(bestValue, minimax(depth-1, board, alpha, beta, not maximizing, first))
            board.pop()
            alpha = max(alpha, bestValue)
            if (beta <= alpha): 
                return bestValue  
                          
        return bestValue

    else:
        bestValue = 9999

        for move in legal_moves:
            board.push(move)
            bestValue = min(bestValue, minimax(depth-1, board, alpha, beta, not maximizing, first))
            board.pop()
            beta = min(beta, bestValue)
            if (beta <= alpha): 
                return bestValue  
                          
        return bestValue

def minimaxroot2(depth, board, maximizing, first):
    global bestMove,origdepth
    bestValue = -9999
    Move = None
    for move in board.legal_moves:
        board.push(move)
        value = minimax2(depth-1, board, -10000, 10000, not maximizing, first)
        board.pop()
        
        if value >= bestValue:
            bestValue = value
            Move = move
    bestMove=Move

def minimax2(depth, board, alpha, beta, maximizing, first):
    if depth == 0:
        return -evaluateBoard(board, first)
    if maximizing:
        bestValue = -9999

        for move in board.legal_moves:
            board.push(move)
            bestValue = max(bestValue, minimax2(depth-1, board, alpha, beta, not maximizing, first))
            board.pop()
            alpha = max(alpha, bestValue)
            if (beta <= alpha): 
                return bestValue  
                          
        return bestValue

    else:
        bestValue = 9999

        for move in board.legal_moves:
            board.push(move)
            bestValue = min(bestValue, minimax2(depth-1, board, alpha, beta, not maximizing, first))
            board.pop()
            beta = min(beta, bestValue)
            if (beta <= alpha): 
                return bestValue  
                          
        return bestValue