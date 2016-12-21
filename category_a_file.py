#!/usr/bin/python

import os

import codecs
#import pandas as pd
#from sklearn import metrics

from passage.preprocessing import Tokenizer
from passage.layers import Embedding, GatedRecurrent, Dense
from passage.models import RNN
from passage.utils import load, save

from load import load_data

trX, teX, trY, teY = load_data(ntrain=9000,ntest=1000) # Can increase up to 250K or so
print len(trX), len(trY), len(teX), len(teY)

print teX.shape()
tokenizer = Tokenizer(min_df=10, max_features=50000)
#print trX[1] # see a blog example
trX = tokenizer.fit_transform(trX)

text = "Evropa je v jeho politika naprosto impotent ."
teX = tokenizer.transform(text)
print "number of tokens:"+str(len(trX));
print "number of feathures:"+ str(tokenizer.n_features)

layers = [
	Embedding(size=256, n_features=tokenizer.n_features),
	GatedRecurrent(size=512, p_drop=0.2),
	Dense(size=10, activation='softmax', p_drop=0.5)
]

model = RNN(layers=layers, cost='cce' ) # bce is classification loss for binary classification and sigmoid output
model = load('modelEcho.pkl') # How to load

te_pred = model.predict(teX)

#tr_acc = metrics.accuracy_score(trY[:len(teY)], tr_preds > 0.5)
#te_acc = metrics.accuracy_score(teY, te_preds > 0.5)

print te_pred
