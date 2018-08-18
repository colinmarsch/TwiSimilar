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

## Fitting Naive Bayes to the Training set ~74% mean cross validation score
#from sklearn.naive_bayes import MultinomialNB
#classifier = MultinomialNB()
#classifier.fit(X_train, y_train)

# Fitting LinearSVC to the Training set ~76.8% mean cross validation score
from sklearn.svm import LinearSVC
classifier = LinearSVC(C = 0.5)
classifier.fit(X_train, y_train)

## Fitting Logistic Regression to the Training Set takes very long time look into this
#from sklearn.linear_model import LogisticRegression
#classifier = LogisticRegression(multi_class = 'multinomial', solver = 'sag')
#classifier.fit(X_train, y_train)

## Fitting Random Forest to the Training Set Low accuracy
#from sklearn.ensemble import RandomForestClassifier
#classifier = RandomForestClassifier(n_estimators = 200, max_depth = 3)
#classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# # Applying k-Fold Cross Validation
# from sklearn.model_selection import cross_val_score
# accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
# accuracies.mean()
# accuracies.std()

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print('Overall Accuracy: ' + str(np.trace(cm) / np.sum(cm)))

# # Applying Grid Search to find the best model and the best parameters
# from sklearn.model_selection import GridSearchCV
# parameters = [{'C': [0.25, 0.5, 1, 10], 'dual': [True, False], 'intercept_scaling': [1, 10]}]
# grid_search = GridSearchCV(estimator = classifier,
#                            param_grid = parameters,
#                            scoring = 'accuracy',
#                            cv = 10,
#                            verbose = 1000)
# grid_search = grid_search.fit(X_train, y_train)
# best_accuracy = grid_search.best_score_
# best_parameters = grid_search.best_params_

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

# Create pickles for classifier and vectorizer
import pickle
filename = 'tweet_classifier.pkl'
model_pickle = open(filename, 'wb')
pickle.dump(classifier, model_pickle)
model_pickle.close()

vectorizer_pickle = open('vectorizer.pkl', 'wb')
pickle.dump(vectorizer, vectorizer_pickle)
vectorizer_pickle.close()