from flask import Flask, redirect, session, request
from flask_cors import CORS
import pickle
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import tweepy
from collections import Counter
nltk.download('stopwords')
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
CORS(app, supports_credentials=True)

@app.route('/')
def authorize():
    # Redirect user to Twitter to authorize
    auth = tweepy.OAuthHandler('SMcVpidT9ypKR8FgPFws6O1Tz', 'LQ7Q5YSEJK6l5jAhTjj1JCi60NSXhT6SWXEIzVlgH3qhfo76wM')
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    session['request_token'] = auth.request_token
    session.modified = True
    return redirect_url

@app.route('/verify')
def predict_similar():
    verifier = request.args.get('oauth_verifier')
    auth = tweepy.OAuthHandler('SMcVpidT9ypKR8FgPFws6O1Tz', 'LQ7Q5YSEJK6l5jAhTjj1JCi60NSXhT6SWXEIzVlgH3qhfo76wM')
    token = session.get('request_token')
    session.pop('request_token')
    auth.request_token = token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
    # Construct the API instance
    api = tweepy.API(auth)
    current_user = api.me()

    tweet_text_list = []
    for i in range(1, 17):
        users_tweets = []
        try:
            users_tweets = api.user_timeline(screen_name = current_user.screen_name, count = 200, page = i)
        except tweepy.error.TweepError:
            break
        if len(users_tweets) == 0:
            break
        for tweet in users_tweets:
            tweet_text = ''.join([i if (ord(i) < 128 and i not in [',', '\n']) else ' ' for i in tweet.text])
            tweet_text = re.sub(r"http\S+", "", tweet_text)
            tweet_text = re.sub('[^a-zA-Z]', ' ', tweet_text).lower().split()
            ps = PorterStemmer()
            tweet_text = [ps.stem(word) for word in tweet_text if not word in set(stopwords.words('english'))]
            tweet_text = ' '.join(tweet_text)
            tweet_text_list.append(tweet_text)

    model_pkl = open('tweet_classifier.pkl', 'rb')
    classifier = pickle.load(model_pkl)
    vectorizer_pkl = open('vectorizer.pkl', 'rb')
    vectorizer = pickle.load(vectorizer_pkl)

    X = vectorizer.transform(tweet_text_list)
    predictions = classifier.predict(X)

    return Counter(predictions).most_common(1)[0]