from flask import Flask
import tweepy

app = Flask(__name__)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

@app.route('/')
def hello_world():
    users_list = []
    current_user = api.me()

    friends_ids = api.friends_ids(screen_name = current_user.screen_name, cursor = -1)
    for auth_friends_id in friends_ids[0]:
        print(auth_friends_id)
        friend = api.get_user(id = auth_friends_id)
        users_list.append(friend)
        mutuals = api.friends_ids(screen_name = friend.screen_name, cursor = -1)
        for id in mutuals[0]:
            print(id)
            mutual = api.get_user(id = id)
            users_list.append(mutual)

    print(users_list)
    return 'Hello, World!'
