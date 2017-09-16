# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics

class Classifier():
    def __init__(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(curr_dir, "labeled_transactions.csv")

        data = loadData(data_path)

        texts, labels = get_XY_from_data(data)
        # split data into train and test
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            texts, labels, test_size=0.4, random_state=0)

        self.model = self.train(self.X_train, self.Y_train)


    def train(self, X_train, Y_train):
        return train_SVM(X_train, Y_train)

    def predict(self, X):
        predicted = self.model.predict(X)
        return [prediction == '1' for prediction in predicted]

    def evaluate(self):
        predicted = self.model.predict(self.X_test)
        # print('SVM: %4f' % np.mean(predicted == Y_test))
        conf_matrixSVM = metrics.confusion_matrix(self.Y_test, predicted)


def loadData(filename):
    return pd.read_csv(filename, encoding="utf-8", sep=";")


# labels are in FailureModeCode
# data under consideration is description text, NotificationInformation
def get_XY_from_data(data):
    X = []
    Y = []
    for i in range(len(data)):
        if (not pd.isnull(data["details"][i])):
            X.append(str(data["details"][i]))
            Y.append(str(data["label"][i]))
    return X, Y


# this function will be replaced when using Pipeline
def tokenize(data):
    countVect = CountVectorizer()
    XTrainCounts = countVect.fit_transform(data)
    tfTransformer = TfidfTransformer(use_idf=False).fit(XTrainCounts)
    XTrainTf = tfTransformer.transform(XTrainCounts)
    return XTrainTf, countVect, tfTransformer


# this function will be replaced when using Pipeline
# def fit_Naive_Bayes(inputs, labels):
#     clf = MultinomialNB().fit(inputs, labels)
#     return clf
#
#
# def train_naive_bayes(X, Y):
#     text_clf = Pipeline([('vect', CountVectorizer()),
#                          ('tfidf', TfidfTransformer()),
#                          ('clf', MultinomialNB()),
#                          ])
#     text_clf = text_clf.fit(X, Y)
#     return text_clf


def train_SVM(X, Y):
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                               alpha=1e-3, n_iter=5, random_state=42)),
                         ])
    text_clf = text_clf.fit(X, Y)
    return text_clf

def buildLabeldistribution(labels):
    dist = []
    s = set(labels)
    for i in s:
        dist.append((i, labels.count(i)))
    return dist
