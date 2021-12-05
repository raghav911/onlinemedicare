import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer

import time
from sklearn import svm
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd

trainData = pd.read_csv("train.csv" , skip_blank_lines=True)

def do_something(val , answer1 , answer2 , answer3):
    # do something
    df = pd.DataFrame(columns=['Content'])
    df.loc[0] = [answer1.strip()]
    df.loc[1] = [answer2.strip()]
    df.loc[2] = [answer3.strip()]
    
    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df = 5,
                                 max_df = 0.8,
                                 sublinear_tf = True,
                                 use_idf = True)

    train_vectors = vectorizer.fit_transform(trainData['Content'])
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, trainData['Label'])
    t1 = time.time()
    test_vectors = vectorizer.transform(df['Content'])
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1

    # results
    print("Results for SVM(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print("prediction_linear:", prediction_linear)

    return prediction_linear[0]

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

