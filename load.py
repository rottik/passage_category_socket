#!/usr/bin/python
import os;
import codecs
import numpy as np
from random import shuffle
def load_data(ntrain=10000, ntest=10000):
    filename = "./category/";
    files = os.walk(filename);
    Y=[]
    X=[]
    labels=[]
    ext=".ltxt"
    for file in os.listdir(filename):
        if file.endswith(ext):
            fo = codecs.open("/".join([filename,file]), "r", "utf-8")
            lines = fo.readlines()
            X.extend(lines);
            Y.extend([file.replace(ext,"")]*len(lines))
            labels.extend([file.replace(ext,"")])
            fo.close()
    print labels
    
    for index in range(len(X)):
        X[index]="\t\t".join([X[index],Y[index]])
    shuffle(X)
    
    for index in range(len(X)):
        [xi, yi]=X[index].split("\t\t")
        X[index]=xi
        theme=np.zeros(len(labels))

        theme[labels.index(yi)]=1.
        Y[index]=theme
        
    trX = X[:-ntest]
    teX = X[-ntest:]
    trY = Y[:-ntest]
    teY = Y[-ntest:]
    return trX, teX, trY, teY

