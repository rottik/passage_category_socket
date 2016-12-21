#!/usr/bin/python

import os
from sklearn import metrics
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
n_cat=10 # replace by real number of categories

tokenizer = Tokenizer(min_df=10, max_features=50000)
trX = tokenizer.fit_transform(trX)
print "number of tokens:"+str(len(trX));
teX = tokenizer.transform(teX)
print "number of feathures:"+ str(tokenizer.n_features)

#layers = [
#    Embedding(size=128, n_features=tokenizer.n_features),
#    GatedRecurrent(size=256, activation='tanh', gate_activation='steeper_sigmoid', init='orthogonal', seq_output=False),
#    Dense(size=1, activation='sigmoid', init='orthogonal') # sigmoid for binary classification
#]

layers = [
	Embedding(size=256, n_features=tokenizer.n_features),
	GatedRecurrent(size=512, p_drop=0.2),
	Dense(size=n_cat, activation='softmax', p_drop=0.5)
]


model = RNN(layers=layers, cost='cce' ) # bce is classification loss for binary classification and sigmoid output
print "RNN prepared"
for i in range(1):
    model.fit(trX, trY, n_epochs=1)
    save(model,'modelEcho.pkl')
    #model = load('modelEcho.pkl')
    tr_preds = model.predict(trX)
    te_preds = model.predict(teX)

    #tr_acc = metrics.accuracy_score(trY[:len(teY)], tr_preds > 0.5)
    #te_acc = metrics.accuracy_score(teY, te_preds > 0.5)

    print trX[0] 
    print trY[0]
    print tr_preds[0]

    file_ = open('train_vec.vec', 'w')
    file_.write(trY)
    file_.close()

    file_ = open('train_pred.vec', 'w')
    file_.write(tr_preds)
    file_.close()

    tr_acc = np.mean(np.argmax(trY) == np.argmax(tr_preds)) 
    te_acc = np.mean(np.argmax(teY) == np.argmax(te_preds))

    # Test accuracy should be between 98.9% and 99.3%
    print 'train accuracy', tr_acc, 'test accuracy', te_acc 

save(model, 'save_model.pkl') # How to save
