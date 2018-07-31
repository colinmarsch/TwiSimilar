from __future__ import division
import numpy as np
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import pandas as pd
dataset = pd.read_csv('Top100Accounts.csv', delimiter = ',', quoting = 3)
dataset = dataset.reindex(np.random.permutation(dataset.index))
X = dataset.iloc[:, 0].values.astype('U')

# Creating a bag of words model
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features = 1500)
X = vectorizer.fit_transform(X).toarray()
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

#  # Fitting Naive Bayes to the Training set
#  from sklearn.naive_bayes import MultinomialNB
#  from imblearn.over_sampling import SMOTE
#  from imblearn.pipeline import Pipeline as imbPipeline
#  classifier = MultinomialNB()
#  classifier = imbPipeline([
#      ('oversample', SMOTE()),
#      ('clf', classifier)
#      ])
#  classifier.fit(X_train, y_train)

## Applying the oversampling algorithm SMOTE and Fitting Kernel SVM to the Training set
#from sklearn.svm import SVC
#from imblearn.over_sampling import SMOTE
#from imblearn.pipeline import Pipeline as imbPipeline
#classifier = SVC(kernel = 'linear')
#classifier = imbPipeline([
#    ('oversample', SMOTE()),
#    ('clf', classifier)
#    ])
#classifier.fit(X_train, y_train)

## Fitting Logistic Regression to the Training Set
#from sklearn.linear_model import LogisticRegression
#from imblearn.over_sampling import SMOTE
#from imblearn.pipeline import Pipeline as imbPipeline
#classifier = LogisticRegression()
#classifier = imbPipeline([
#    ('oversample', SMOTE()),
#    ('clf', classifier)
#    ])
#classifier.fit(X_train, y_train)

# Fitting Random Forest to the Training Set
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imbPipeline
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier = imbPipeline([
    ('oversample', SMOTE()),
    ('clf', classifier)
    ])
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print('Overall Accuracy: ' + str(np.trace(cm) / np.sum(cm)))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))