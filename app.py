import tweepy
import csv
import re
import numpy as np
import pandas as pd
from __future__ import division
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

users_list = []
current_user = api.get_user(screen_name = 'colinmarsch')

# # Get all the tweets of the account that is specified
# print('Getting all the tweets of the specified user.')
# with open('tweets.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['Tweet', 'User'])
#     for i in range(1, 51):
#         print("Page: " + str(i) + "/" + str(50))
#         try:
#             tweets = api.user_timeline(screen_name = current_user.screen_name, count = 1000, page = i)
#         except tweepy.error.TweepError:
#             print("Couldn't access the tweets of the currently selected account.")
#             break
#         if len(tweets) == 0:
#             break
#         current_tweet_list = []
#         for tweet in tweets:
#             text_val = ''.join([i if (ord(i) < 128 and i not in [',', '\n']) else ' ' for i in tweet.text])
#             text_val = re.sub('[^a-zA-Z]', ' ', text_val).lower().split()
#             ps = PorterStemmer()
#             text_val = [ps.stem(word) for word in text_val if not word in set(stopwords.words('english'))]
#             text_val = ' '.join(text_val)
#             writer.writerow([text_val, current_user.screen_name])

# # Get all the users that the account follows
# print('Getting all the users that the account follows')
# friends_ids = api.friends_ids(screen_name = current_user.screen_name, cursor = -1)
# counter = 0
# for auth_friends_id in friends_ids[0]:
#     counter = counter + 1
#     print("Getting Users: " + str(counter) + "/" + str(len(friends_ids[0])))
#     friend = api.get_user(id = auth_friends_id)
#     users_list.append(friend)

# # Get all the tweets of the users that the account follows
# print('Getting all the tweets of the users that the account follows.')
# counter = 0
# with open('users.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['Tweet', 'User'])
#     for user in users_list:
#         counter = counter + 1
#         print("Writing CSV: " + str(counter) + "/" + str(len(users_list)))
#         tweet_text_list = []
#         for i in range(1, 51):
#             print("Page: " + str(i) + "/" + str(50))
#             users_tweets = []
#             try:
#                 users_tweets = api.user_timeline(screen_name = user.screen_name, count = 1000, page = i)
#             except tweepy.error.TweepError:
#                 print("Couldn't access the tweets of " + user.screen_name)
#                 break
#             if len(users_tweets) == 0:
#                 break
#             for tweet in users_tweets:
#                 text_val = ''.join([i if (ord(i) < 128 and i not in [',', '\n']) else ' ' for i in tweet.text])
#                 text_val = re.sub('[^a-zA-Z]', ' ', text_val).lower().split()
#                 ps = PorterStemmer()
#                 text_val = [ps.stem(word) for word in text_val if not word in set(stopwords.words('english'))]
#                 text_val = ' '.join(text_val)
#                 writer.writerow([text_val, user.screen_name])


dataset = pd.read_csv('users.csv', delimiter = ',', quoting = 3)
X = dataset.iloc[:, 0].values.astype('U')

# Creating a bag of words model
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features = 1500)
X = vectorizer.fit_transform(X).toarray()
y = dataset.iloc[:, 1].values

from imblearn.over_sampling import SMOTE, RandomOverSampler
X, y = RandomOverSampler().fit_sample(X, y)
X, y = SMOTE().fit_sample(X, y)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Naive Bayes to the Training set
#from sklearn.naive_bayes import MultinomialNB
#classifier = MultinomialNB()
#classifier.fit(X_train, y_train)

# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf')
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print('Overall Accuracy: ' + str(np.trace(cm) / np.sum(cm)))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))