#!/usr/bin/python

import os
import pandas as pd
import pickle
import numpy as np

from passage.preprocessing import Tokenizer
from passage.layers import Embedding, GatedRecurrent, Dense
from passage.models import RNN
from passage.utils import load, save

from load import load_data
#################
# training data have to be lemmatized using Morphodita !!!!!!!!!
#################
trX, teX, trY, teY = load_data(ntrain=9000,ntest=1000)
print len(trX), len(trY), len(teX), len(teY)

tokenizer = Tokenizer(min_df=10, max_features=50000)
trX = tokenizer.fit_transform(trX)
pickle.dump(tokenizer,open('tokenizer.pkl', 'wb'))
print "number of tokens:"+str(len(trX));
teX = tokenizer.transform(teX)
print "number of feathures:"+ str(tokenizer.n_features)

layers = [
	Embedding(size=256, n_features=tokenizer.n_features),
	GatedRecurrent(size=725),
	Dense(size=10, activation='softmax')
]

model = RNN(layers=layers, cost='cce' )
model.fit(trX, trY, n_epochs=10)
save(model,'modelEcho.pkl')

tr_preds = model.predict(trX)
te_preds = model.predict(teX)

data=pd.DataFrame(trY)
data.to_csv('data/trY.vec')

data=pd.DataFrame(tr_preds)
data.to_csv('data/tr_preds.vec')

tr_acc = np.mean(np.argmax(trY,axis=1) == np.argmax(tr_preds,axis=1)) 
indexy=np.argmax(teY,axis=1)
data= pd.DataFrame(indexy)
data.to_csv('data/ev_agrmax.txt')
data= pd.DataFrame(np.argmax(te_preds,axis=1))
data.to_csv('data/ev_pred_agrmax.txt')

te_acc = np.mean(np.argmax(teY,axis=1) == np.argmax(te_preds,axis=1))

print 'train accuracy', tr_acc, 'test accuracy', te_acc 
