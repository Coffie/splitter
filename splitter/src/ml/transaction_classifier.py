# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import numpy as  np
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

def main():
    data = loadData("data/NotificationInformation.csv")
    texts, labels = get_XY_from_data(data)
    # split data into train and test
    X_train, X_test, Y_train, Y_test = train_test_split(
        texts, labels, test_size=0.4, random_state=0)

    modelLR = train_LR(X_train, Y_train)
    predicted = modelLR.predict(X_test)
    print('Logistic Regression: %4f' % np.mean(predicted == Y_test))
    conf_matrixNB = metrics.confusion_matrix(Y_test, predicted)

    modelNB = train_naive_bayes(X_train, Y_train)
    predicted = modelNB.predict(X_test)
    print('Naive Bayes : %4f' % np.mean(predicted == Y_test))
    conf_matrixNB = metrics.confusion_matrix(Y_test, predicted)

    # TODO: change to LDA
    modelSVM = trainSVM(X_train, Y_train)
    predicted = modelSVM.predict(X_test)
    print('SVM: %4f' % np.mean(predicted == Y_test))
    conf_matrixSVM = metrics.confusion_matrix(Y_test, predicted)

    gs_clf = performVectorizerGridSearch(modelLR, X_train, Y_train)
    predicted = gs_clf.predict(X_test)
    print("Best score on lr: %.4f" % np.mean(predicted == Y_test))
    print('Best score on LR: %4f' % gs_clf.best_score_)
    print(gs_clf.best_params_)

    gs_clf = performGridSearch(modelNB, X_train, Y_train)
    predicted = gs_clf.predict(X_test)
    print("Best score on NB: %.4f" % np.mean(predicted == Y_test))
    print(gs_clf.best_params_)

    gs_clf = performGridSearch(modelSVM, X_train, Y_train)
    predicted = gs_clf.predict(X_test)
    print("Best score on SVM: %.4f" % np.mean(predicted == Y_test))
    print(gs_clf.best_params_)
    # it is 0.48808
    # for param_name in sorted(parameters.keys()):
    # print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
    # clf__alpha: 0.001
    # tfidf__use_idf: True
    # vect__ngram_range: (1, 6)

def loadData(filename):
    return pd.read_csv(filename, encoding="latin-1")


# labels are in FailureModeCode
# data under consideration is description text, NotificationInformation
def get_XY_from_data(data):
    texts = []
    labels = []
    for i in range(len(data)):
        if (not pd.isnull(data["FailureModeCode"][i])):
            labels.append(str(data["FailureModeCode"][i]))
            texts.append(str(data["NotificationInformation"][i]) +
                         str(data["Description"][i]) +
                         str(data["Text"][i]) + " " +
                         str(data["OrderType"][i]) + " " +
                         str(data["CatalogProfile_Id"][i]) + " " +
                         str(data["Plant"][i])
                         )
    return texts, labels


# this function will be replaced when using Pipeline
def tokenize(data):
    countVect = CountVectorizer()
    XTrainCounts = countVect.fit_transform(data)
    tfTransformer = TfidfTransformer(use_idf=False).fit(XTrainCounts)
    XTrainTf = tfTransformer.transform(XTrainCounts)
    return XTrainTf, countVect, tfTransformer


# this function will be replaced when using Pipeline
def fit_Naive_Bayes(inputs, labels):
    clf = MultinomialNB().fit(inputs, labels)
    return clf


def train_naive_bayes(X, Y):
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                         ])
    text_clf = text_clf.fit(X, Y)
    return text_clf


def train_SVM(X, Y):
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                               alpha=1e-3, n_iter=5, random_state=42)),
                         ])
    text_clf = text_clf.fit(X, Y)
    return text_clf


def train_LR(X, Y):
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', LogisticRegression()),
                         ])
    text_clf = text_clf.fit(X, Y)
    return text_clf


def predictNewIntances(testset, countVect, tfTransformer, model):
    XNewCounts = countVect.transform(testset)
    XNewTfidf = tfTransformer.transform(XNewCounts)
    predicted = model.predict(XNewTfidf)
    return predicted


def buildLabeldistribution(labels):
    dist = []
    s = set(labels)
    for i in s:
        dist.append((i, labels.count(i)))
    return dist


def performGridSearch(model, X_train, Y_train):
    parameters = {'vect__ngram_range': [(1, 2), (1, 3), (1, 4)],
                  'tfidf__use_idf': (True, False),
                  # 'clf__alpha': (1e-2, 1e-3),
                  }
    gs_clf = GridSearchCV(model, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(X_train, Y_train)
    return gs_clf


def performVectorizerGridSearch(model, X_train, Y_train):
    parameters = {'vect__ngram_range': [(1, 2), (1, 3), (1, 4)],
                  'tfidf__use_idf': (True, False),
                  'vect__max_features': [x for x in range(4000, 5001, 500)]}
    gs_clf = GridSearchCV(model, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(X_train, Y_train)
    return gs_clf


if __name__ == "__main__":
    main()
