from __future__ import division
import numpy as np
import pandas as pd

dataset = pd.read_csv('Top10Accounts.csv', delimiter = ',', quoting = 3)
dataset = dataset.reindex(np.random.permutation(dataset.index))
X = dataset.iloc[:, 0].values.astype('U')

# Creating a bag of words model
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range = (1,2), max_features = 50000)
X = vectorizer.fit_transform(X).toarray()
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15, random_state = 0)

## Fitting Naive Bayes to the Training set
#from sklearn.naive_bayes import MultinomialNB
#classifier = MultinomialNB()
#classifier.fit(X_train, y_train)

# Fitting LinearSVC to the Training set ~75%
from sklearn.svm import LinearSVC
classifier = LinearSVC()
classifier.fit(X_train, y_train)

## Fitting Logistic Regression to the Training Set
#from sklearn.linear_model import LogisticRegression
#classifier = LogisticRegression(multi_class = 'ovr', solver = 'sag')
#classifier.fit(X_train, y_train)

## Fitting Random Forest to the Training Set
#from sklearn.ensemble import RandomForestClassifier
#classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy')
#classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print('Overall Accuracy: ' + str(np.trace(cm) / np.sum(cm)))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))