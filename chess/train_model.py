from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder,LabelEncoder
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import pickle
from AI import getPieceValue
import chess

df = pd.read_csv('data.csv')
for i in range(64):
    oldV=['None']
    newV=[0]
    for k in chess.PIECE_SYMBOLS[1:]:
        v=getPieceValue(k,i//8,i%8,True)
        oldV+=[k,k.upper()]
        newV+=[v,-v]
    df.iloc[:,i].replace(oldV,newV,inplace=True)

X,Y=df.drop(columns=['good_move']),df['good_move']

lg = LogisticRegression(max_iter=10000)
lg.fit(X,Y)
filename = 'model.sav'
pickle.dump(lg,open(filename,'wb'))

# if __name__=='__main__':
#     df = pd.read_csv('data.csv')
#     X,Y=df.drop(columns=['good_move']),df['good_move']
#     enc=OrdinalEncoder()
#     enc.fit(X)
#     x=enc.transform(X)
#     enc2=LabelEncoder()
#     enc2.fit(Y)
#     y=enc2.transform(Y)

#     X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.25)
#     nb = CategoricalNB()
#     nb.fit(X_train, Y_train)
#     print(nb.score(X_test,Y_test))
#     filename = 'model.sav'
#     pickle.dump(nb,open(filename,'wb'))
#     filename2 = 'enc.sav'
#     pickle.dump(enc,open(filename2,'wb'))

# def predict_DF(dfx,model,enc):
#     toPredict=[]
#     gotIdx=[]
#     noGotIdx=[]
#     for j in range(len(dfx)):
#         nrow=np.zeros(192)
#         for i in range(len(enc.categories_)):
#             idx=np.where(enc.categories_[i]==dfx[j][i])[0]
#             if len(idx)==0:
#                 nrow=None
#                 break
#             nrow[i]=idx[0]
#         if nrow is None: 
#             noGotIdx.append(j)
#             continue
#         toPredict.append(nrow)
#         gotIdx.append(j)
#     if len(toPredict)==0:
#         nl =[[noGotIdx[j],0.5] for j in range(len(noGotIdx))]
#     else:
#         toPredict=np.array(toPredict)
#         gotPred=list(model.predict_proba(toPredict))
#         nl = [[gotIdx[i],gotPred[i][0]] for i in range(len(gotIdx))]+[[noGotIdx[j],0.5] for j in range(len(noGotIdx))]
#         nl.sort(key=lambda x: -x[1])
#     return nl
