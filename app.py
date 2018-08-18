from flask import Flask
import pickle
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
app = Flask(__name__)

@app.route('/<tweet>')
def predict_similar(tweet):
    model_pkl = open('tweet_classifier.pkl', 'rb')
    classifier = pickle.load(model_pkl)
    vectorizer_pkl = open('vectorizer.pkl', 'rb')
    vectorizer = pickle.load(vectorizer_pkl)

    tweet_text = ''.join([i if (ord(i) < 128 and i not in [',', '\n']) else ' ' for i in tweet])
    tweet_text = re.sub(r"http\S+", "", tweet_text)
    tweet_text = re.sub('[^a-zA-Z]', ' ', tweet_text).lower().split()
    ps = PorterStemmer()
    tweet_text = [ps.stem(word) for word in tweet_text if not word in set(stopwords.words('english'))]
    tweet_text = ' '.join(tweet_text)
    X = vectorizer.transform([tweet_text])

    return classifier.predict(X)[0]