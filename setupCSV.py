import tweepy
import csv
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

# Get last 1000 tweets from the top 100 accounts
with open('top10.txt') as top100:
    top100_accounts = top100.readlines()
top100_accounts = [x[1:].strip() for x in top100_accounts]
counter = 0
with open('Top10Accounts.csv', 'wb') as csvfile:
   writer = csv.writer(csvfile, delimiter=',')
   writer.writerow(['Tweet', 'User'])
   for screen_name in top100_accounts:
       counter = counter + 1
       print("Writing CSV: " + str(counter) + "/" + str(len(top100_accounts)))
       tweet_text_list = []
       for i in range(1, 17):
           print("Page: " + str(i) + "/" + str(16))
           users_tweets = []
           try:
               users_tweets = api.user_timeline(screen_name = screen_name, count = 200, page = i)
           except tweepy.error.TweepError:
               print("Couldn't access the tweets of " + screen_name)
               break
           if len(users_tweets) == 0 or (len(users_tweets) < 100 and i == 1):
               break
           for tweet in users_tweets:
               tweet_text = ''.join([i if (ord(i) < 128 and i not in [',', '\n']) else ' ' for i in tweet.text])
               tweet_text = re.sub(r"http\S+", "", tweet_text)
               tweet_text = re.sub('[^a-zA-Z]', ' ', tweet_text).lower().split()
               ps = PorterStemmer()
               tweet_text = [ps.stem(word) for word in tweet_text if not word in set(stopwords.words('english'))]
               tweet_text = ' '.join(tweet_text)
               writer.writerow([tweet_text, screen_name])