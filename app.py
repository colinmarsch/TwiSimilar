import tweepy
import csv

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

users_list = []
current_user = api.me()

friends_ids = api.friends_ids(screen_name = current_user.screen_name, cursor = -1)
counter = 0
for auth_friends_id in friends_ids[0]:
    counter = counter + 1
    print("Getting Users:" + str(counter) + "/" + str(len(friends_ids[0])))
    friend = api.get_user(id = auth_friends_id)
    users_list.append(friend)
    # this takes a long time, figure out better way to show progress
    # mutuals = api.friends_ids(screen_name = friend.screen_name, cursor = -1)
    # for id in mutuals[0]:
    #     mutual = api.get_user(id = id)
    #     users_list.append(mutual)

counter = 0
with open('users.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['UserID'])
    for user in users_list:
        counter = counter + 1
        print("Writing CSV:" + str(counter) + "/" + str(len(users_list)))
        # add loop here to get more of each users tweets, need to make sure there are still tweets left
        users_tweets = api.user_timeline(screen_name = user.screen_name, count = 20, page = 1)
        tweet_text_list = []
        for tweet in users_tweets:
            text_val = ''.join([i if (ord(i) < 128 and i not in [',', '\n']) else ' ' for i in tweet.text])
            tweet_text_list.append(text_val)
        writer.writerow([user.screen_name] + tweet_text_list)
