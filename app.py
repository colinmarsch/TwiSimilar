from flask import Flask
import tweepy

app = Flask(__name__)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

@app.route('/')
def hello_world():
    return 'Hello, World!'
