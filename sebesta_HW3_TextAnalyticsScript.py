'''
Title: sebesta_HW3_TextAnalyticsScript
Author: Kalea Sebesta
Date: 11/15/2017
Due Date: 11/28/2015

Purpose:
Part 1,
Using the three provided documents (Gutenberg books (UTF-8, text docs) of Hamlet,
Macbeth, and Pinocchio) write Python code to accomplish the following:
1). Tokenize (word level) the documents.
2). Remove punctuation and case normalize (to lower case) the token vectors.
3). Apply stopword removal (using NLTK’s standard “English” stopword list).
4). Apply Porter’s stemming algorithm to the stopword filtered lexicon.
5). Create a vector space representation of the documents using the reduced
dimension feature set (case normalized, minus stopwords, with stemming applied).
    a). First with binary dimensions.
    b). Second with dimension values equal to raw term frequency (TF).
    c). Third with dimension values equal to normalized term frequency
    (normalized on [0-1] scale.
    d). Fourth with dimension values equal to TF-IDF (TFxIDF).
6). Calculate the cosine similarity between each pair of documents.
'''
# -----------------------------------------------------------------------------
# import libraries/collections
import nltk
import os
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy import spatial
import numpy as np
from nltk import FreqDist
# -----------------------------------------------------------------------------

# set dir and read in txt files from directory
# open and read docs
os.chdir("/Volumes/UTSA QRT2/IS 6713 Data Foundations/Assignments/HW3")
hamlet = open("HW3-Hamlet.txt").read()
macbeth = open("HW3-Macbeth.txt").read()
pino = open("HW3-Pinocchio.txt").read()
# -----------------------------------------------------------------------------

# tokenize (word level) in Hamlet
ham_tok = word_tokenize(hamlet)
print(len(ham_tok))
print(len(set(ham_tok)))

# tokenize (word level) in Macbeth
mac_tok = word_tokenize(macbeth)
print(len(mac_tok))
print(len(set(mac_tok)))

# tokenize (word level) in Pinocchio
pin_tok = word_tokenize(pino)
print(len(pin_tok))
print(len(set(pin_tok)))
# -----------------------------------------------------------------------------

# case normalization & calculating the lexical diveristy (% of unique words in the vocab)
ham_tok_norm = [w.lower() for w in ham_tok if w.isalnum()]
token = len(ham_tok_norm)
unique = len(set(ham_tok_norm))
print(len(ham_tok_norm))
print(len(set(ham_tok_norm)))
lexical_diversity = unique/token

mac_tok_norm = [w.lower() for w in mac_tok if w.isalnum()]
token = len(mac_tok_norm)
unique = len(set(mac_tok_norm))
print(len(mac_tok_norm))
print(len(set(mac_tok_norm)))
lexical_diversity = unique/token

pin_tok_norm = [w.lower() for w in pin_tok if w.isalnum()]
token = len(pin_tok_norm)
unique = len(set(pin_tok_norm))
print(len(pin_tok_norm))
print(len(set(pin_tok_norm)))
lexical_diversity = unique/token
# -----------------------------------------------------------------------------

# stopword removal English stopword list
stop=set(stopwords.words('english'))
# initalize a new list for each doc to remove stopwords
ham_tok_norm_stop = []
mac_tok_norm_stop = []
pin_tok_norm_stop = []

# removing stop words for hamlet
for w in ham_tok_norm:
    if w not in stop:
        ham_tok_norm_stop.append(w)
token = len(ham_tok_norm_stop)
unique = len(set(ham_tok_norm_stop))

# removing stop words for macbeth
for w in mac_tok_norm:
    if w not in stop:
        mac_tok_norm_stop.append(w)
token = len(mac_tok_norm_stop)
unique = len(set(mac_tok_norm_stop))

# removing stop words for pinocchio
for w in pin_tok_norm:
    if w not in stop:
        pin_tok_norm_stop.append(w)
token = len(pin_tok_norm_stop)
unique = len(set(pin_tok_norm_stop))
# -----------------------------------------------------------------------------

# Porter's stemming alg to stopword lexicon
# replacing features that contain the same root
porter = nltk.PorterStemmer()
ham_tok_norm_stop_stem = [porter.stem(w) for w in ham_tok_norm_stop]
token = len(ham_tok_norm_stop_stem)
unique = len(set(ham_tok_norm_stop_stem))

mac_tok_norm_stop_stem = [porter.stem(w) for w in mac_tok_norm_stop]
token = len(mac_tok_norm_stop_stem)
unique = len(set(mac_tok_norm_stop_stem))

pin_tok_norm_stop_stem = [porter.stem(w) for w in pin_tok_norm_stop]
token = len(pin_tok_norm_stop_stem)
unique = len(set(pin_tok_norm_stop_stem))
# -----------------------------------------------------------------------------

# create vector space representation of the documents
# for each word in each document, if the word is not in the vector for all
# words in all documents it is added to the vector
tok_norm_stop_stem = []
for w in ham_tok_norm_stop_stem:
    if w not in tok_norm_stop_stem:
        tok_norm_stop_stem.append(w)
for w in mac_tok_norm_stop_stem:
    if w not in tok_norm_stop_stem:
        tok_norm_stop_stem.append(w)
for w in pin_tok_norm_stop_stem:
    if w not in tok_norm_stop_stem:
        tok_norm_stop_stem.append(w)

# creating a vector that holds the unique words in the vocabulary
lexicon = set(tok_norm_stop_stem)
# calculating the length of the unique words vector
lexicon_dim = len(lexicon)

# creating empty header row
termvect_binary_terms = []
# -----------------------------------------------------------------------------

# a) with binary dimensions
# create separate empty vector for each document
termvect_binary_ham = []
termvect_binary_mac = []
termvect_binary_pin = []

# for each word in the unique word vector, it checks if the word exists in each
# document. If it is in a document a 1 is appened to the binary doc vector, if
# not a zero is added to the vector.
for c in lexicon:
    termvect_binary_terms.append(c)
    if c in ham_tok_norm_stop_stem:
        termvect_binary_ham.append(1)
    if c not in ham_tok_norm_stop_stem:
        termvect_binary_ham.append(0)
    if c in mac_tok_norm_stop_stem:
        termvect_binary_mac.append(1)
    if c not in mac_tok_norm_stop_stem:
        termvect_binary_mac.append(0)
    if c in pin_tok_norm_stop_stem:
        termvect_binary_pin.append(1)
    if c not in pin_tok_norm_stop_stem:
        termvect_binary_pin.append(0)

# initialize counter
count = 0
# creates a binary matrix with zeros and then loops through each word
# in the unique word vector. If that word exists in each document a 1
# is to that index for the corresponding document.
# range depends on the number of rows (doc dealing with)
matrix_binary = [[0 for c in range(lexicon_dim)] for r in range(4)]
for c in lexicon:
    # putting the words in the header row
    matrix_binary[0][count] = c
    if c in ham_tok_norm_stop_stem:
        matrix_binary[1][count] = 1
    if c in mac_tok_norm_stop_stem:
        matrix_binary[2][count] = 1
    if c in pin_tok_norm_stop_stem:
        matrix_binary[3][count] = 1
    count=count+1
print(matrix_binary)
# -----------------------------------------------------------------------------

# b) with dimension values equal to raw term frequency (TF)
count = 0
# creates the matrix_TF with zeros and then adds the frequency count for each
# word in each document at the corresponding index
matrix_TF = [[0 for c in range(lexicon_dim)] for r in range(4)]
for c in lexicon:
    matrix_TF[0][count] = c
    # count number of times word 'c' is in the list
    matrix_TF[1][count] = ham_tok_norm_stop_stem.count(c)
    matrix_TF[2][count] = mac_tok_norm_stop_stem.count(c)
    matrix_TF[3][count] = pin_tok_norm_stop_stem.count(c)
    count = count+1
print(matrix_TF)
# -----------------------------------------------------------------------------

# c) with dimension values equal to normalized term frequency (normalized on[0-1] scale).
# TF_norm...value is count/total tokens
# creates the matrix_TF_norm with zeros and counts the normalized term frequency
# for each document.
count = 0
total_tokens = len(lexicon)
matrix_TF_norm = [[0 for c in range(lexicon_dim)] for r in range(4)]
for c in lexicon:
    matrix_TF_norm[0][count] = c
    matrix_TF_norm[1][count] = ham_tok_norm_stop_stem.count(c)/len(ham_tok_norm_stop_stem)
    matrix_TF_norm[2][count] = mac_tok_norm_stop_stem.count(c)/len(mac_tok_norm_stop_stem)
    matrix_TF_norm[3][count] = pin_tok_norm_stop_stem.count(c)/len(pin_tok_norm_stop_stem)
    count = count+1
print(matrix_TF_norm)
# -----------------------------------------------------------------------------

# d) with dimension values equal to TF-IDF (TFxIDF)
# for IDF you have to create an IDF vector
# initializing IDF vector
vector_idf = []
# run through loop for each token in lexicon
for i in range(lexicon_dim):
    # df=doc frequency this is like n_t...number of docs that term exists in
    df = 0
    if matrix_binary[1][i] == 1:
        df = df+1
    if matrix_binary[2][i] == 1:
        df = df+1
    if matrix_binary[3][i] == 1:
        df = df+1

    # creating the IDF value
    # numerator is N (the number of docs, or number of rows in the matrix
    # minus the header row)
    idf = math.log(3/(df))
    # added IDF values together
    vector_idf.append(idf)
vector_idf

# created a separate for loop to get the term frequencies from matrix_TF_norm
# and multiply it against its respective value in the vector IDF
count = 0
matrix_TF_IDF = [[0 for c in range(lexicon_dim)] for r in range(4)]
for c in lexicon:
    matrix_TF_IDF[0][count] = c
    matrix_TF_IDF[1][count] = (ham_tok_norm_stop_stem.count(c)/len(ham_tok_norm_stop_stem))*vector_idf[count]
    matrix_TF_IDF[2][count] = (mac_tok_norm_stop_stem.count(c)/len(mac_tok_norm_stop_stem))*vector_idf[count]
    matrix_TF_IDF[3][count] = (pin_tok_norm_stop_stem.count(c)/len(pin_tok_norm_stop_stem))*vector_idf[count]
    count = count+1
print(matrix_TF_IDF[1])
# -----------------------------------------------------------------------------

# Text Analysis Question 2c.
# calculate cosine similarity between each pair of documents
# ham and mac
cosine_ham_mac=spatial.distance.cosine(matrix_TF_IDF[1], matrix_TF_IDF[2])
# ham and pin
cosine_ham_pin=spatial.distance.cosine(matrix_TF_IDF[2], matrix_TF_IDF[3])
# mac and pin
cosine_mac_pin=spatial.distance.cosine(matrix_TF_IDF[1], matrix_TF_IDF[3])

print("distance H-M, ",cosine_ham_mac)
print("distance H-P, ",cosine_ham_pin)
print("distance M-P, ",cosine_mac_pin)
# -----------------------------------------------------------------------------

# Text Analysis Question 2b.
# ten most important terms in each document (in rank order)
# Do they change when measuring raw TF, normalized TF, and TF-IDF
# calculate frequency distribution of terms raw
fdistham = FreqDist(ham_tok)
fdistmac = FreqDist(mac_tok)
fdistpin = FreqDist(pin_tok)
print(fdistham)
print(fdistmac)
print(fdistpin)
#show most frequent 10 tokens
fdistham.most_common(10)
fdistmac.most_common(10)
fdistpin.most_common(10)
#plot cumulatively the most frequent 10 tokens
fdistham.plot(10,cumulative=True)
fdistmac.plot(10,cumulative=True)
fdistpin.plot(10,cumulative=True)
#plot NOT cumulatively the most frequent 10 tokens
fdistham.plot(10)
fdistmac.plot(10)
fdistpin.plot(10)

# calculate frequency distribution of terms normalized
fdistham_norm = FreqDist(ham_tok_norm)
fdistmac_norm = FreqDist(mac_tok_norm)
fdistpin_norm = FreqDist(pin_tok_norm)
print(fdistham_norm)
print(fdistmac_norm)
print(fdistpin_norm)
#show most frequent 10 tokens
fdistham_norm.most_common(10)
fdistmac_norm.most_common(10)
fdistpin_norm.most_common(10)
#plot cumulatively the most frequent 10 tokens
fdistham_norm.plot(10,cumulative=True)
fdistmac_norm.plot(10,cumulative=True)
fdistpin_norm.plot(10,cumulative=True)
#plot NOT cumulatively the most frequent 10 tokens
fdistham_norm.plot(10)
fdistmac_norm.plot(10)
fdistpin_norm.plot(10)


# calculate frequency distribution of terms TF-IDF
fdistham_norm_stop_stem = FreqDist(ham_tok_norm_stop_stem)
fdistmac_norm_stop_stem = FreqDist(mac_tok_norm_stop_stem)
fdistpin_norm_stop_stem = FreqDist(pin_tok_norm_stop_stem)
print(fdistham_norm_stop_stem)
print(fdistmac_norm_stop_stem)
print(fdistpin_norm_stop_stem)
#show most frequent 10 tokens
fdistham_norm_stop_stem.most_common(10)
fdistmac_norm_stop_stem.most_common(10)
fdistpin_norm_stop_stem.most_common(10)
#plot cumulatively the most frequent 10 tokens
fdistham_norm_stop_stem.plot(10,cumulative=True)
fdistmac_norm_stop_stem.plot(10,cumulative=True)
fdistpin_norm_stop_stem.plot(10,cumulative=True)
#plot NOT cumulatively the most frequent 10 tokens
fdistham_norm_stop_stem.plot(10)
fdistmac_norm_stop_stem.plot(10)
fdistpin_norm_stop_stem.plot(10)
# -----------------------------------------------------------------------------