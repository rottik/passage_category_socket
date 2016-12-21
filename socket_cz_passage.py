'''
    Classification server
    args: tagger_file rnn_model_file
'''
import pickle
import socket
import time
import sys
from thread import *
import os
import codecs
from random import shuffle
import numpy as np
from passage import preprocessing
from passage.preprocessing import Tokenizer
from passage.layers import Embedding, GatedRecurrent, Dense
from passage.models import RNN
from passage.utils import load, save
from ufal.morphodita import *


######################################################################################################
# methods
    
def encode_entities(text):
  return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def clientthread(conn):
    buffersize=1024
    attack=False
    data =""
    while True:
        datatmp = conn.recv(buffersize)
        datatmp = datatmp.strip()
        #empty line ends read
        if(datatmp=="EOF"):
            break
        data+=datatmp
    if len(data) > (2*1024*buffersize*6): #2048 * buffer UTF-8 znaku
        print "attack"
        attack=True;
        return
                        
    # Lemmatize TEXT
    
    lemmatizedText=LemmatizeText(data)
    
    # Run classification
    reply=ClassifyWithPassage(lemmatizedText, rich=True)
    conn.sendall(reply)
    conn.close()  
    
    
def ClassifyWithPassage(text,rich=False):
    l=[]
    l.append(text)
    te = tokenizerRNN.transform(l)
    te_preds = model.predict(te)
    maxIndex = np.argmax(te_preds)
    if(rich==False):
        return labels[maxIndex]
    else:
        reply="<table><tr>"
        for label in labels:
            reply+="<th>%s</th>" % label
        reply += "</tr><tr>"
        for pred in te_preds:
            reply+="<td>%f</td>" % pred
        reply += "</tr></table>"
        print reply
    return reply

    
def LemmatizeText(text):
    formsMorp = Forms()
    lemmasMorp = TaggedLemmas()
    tokensMorp = TokenRanges()
    tokenizerMorp = taggerMorp.newTokenizer()
    if tokenizerMorp is None:
        sys.stderr.write("No tokenizer is defined for the supplied model!")
        sys.exit(1)
        
    tokenizerMorp.setText(data)
    lemmatizedText="";
    while tokenizerMorp.nextSentence(formsMorp, tokensMorp):
        taggerMorp.tag(formsMorp, lemmasMorp)
        for i in range(len(lemmasMorp)):
            lemmaMorp = lemmasMorp[i]
            lemmatizedText+=encode_entities(lemmaMorp.lemma.split("_")[0].split("-")[0])+" "
    lemmatizedText = lemmatizedText.strip()
    return lemmatizedText
    
##########################################################################################################
# inicializace 
if __name__ == "__main__":
    HOST = ''   # Symbolic name meaning all available interfaces
    PORT = 8888 # Arbitrary non-privileged port
    labels=[]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.bind((HOST, PORT))
            break
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message: ' + msg[1]
            time.sleep( 5 )
    print 'Socket created'

    # Init tagger
    print "Loading tagger..."
    taggerMorp = Tagger.load(sys.argv[1])
    if not taggerMorp:
        sys.stderr.write("Cannot load tagger from file '%s'\n" % sys.argv[1])
        sys.exit(1)

    # Init RNN
    print "Loading RNN..."
    tokenizerRNN = pickle.load(open('tokenizer.pkl', 'rb'))

    layers = [
        Embedding(size=256, n_features=tokenizerRNN.n_features),
        GatedRecurrent(size=512, p_drop=0.2),
        Dense(size=10, activation='softmax', p_drop=0.5)
    ]

    model = RNN(layers=layers, cost='cce' ) # bce is classification loss for binary classification and sigmoid output
    model = load(sys.argv[2]) # How to load
    print "RNN loaded"


    s.listen(10)
    print 'Socket now listening'
    #######################################################################################################
    while 1:
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        start_new_thread(clientthread ,(conn,))
    s.close()
