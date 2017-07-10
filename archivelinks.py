#!/usr/bin/env python3

# Listens to a Twitter timeline and sends tweeted URLs to the Internet Archive.

import os
import requests
import yaml
from twython import Twython, TwythonStreamer, TwythonError

fullpath = os.path.dirname(os.path.realpath(__file__))
CONFIG = os.path.join(fullpath, "config.yaml")

def get_config():
    with open(CONFIG,'r') as c:
        config = yaml.load(c)
    return config

def get_stream_instance(config):
    twitter_app_key = config['twitter_app_key']
    twitter_app_secret = config['twitter_app_secret']
    twitter_oauth_token = config['twitter_oauth_token']
    twitter_oauth_token_secret = config['twitter_oauth_token_secret']
    return TwythonStreamer(twitter_app_key, twitter_app_secret, twitter_oauth_token, twitter_oauth_token_secret)

def get_twitter_instance(config):
    twitter_app_key = config['twitter_app_key']
    twitter_app_secret = config['twitter_app_secret']
    twitter_oauth_token = config['twitter_oauth_token']
    twitter_oauth_token_secret = config['twitter_oauth_token_secret']
    return Twython(twitter_app_key, twitter_app_secret, twitter_oauth_token, twitter_oauth_token_secret)

def check_tweet(data):
    if 'entities' in data:
        url_list = grab_urls(data)
        for url in url_list:
            archive_link = send_to_archive(url)
            if any(t['screen_name'] == 'LinkArchiver' for t in data['entities']['user_mentions']):
                tweet_reply(archive_link, data['id_str'], 
                        data['user']['screen_name'])
    elif 'event' in data:
        print("Some kind of event!")
        if data['event'] == 'follow' and data['source']['screen_name'] != 'LinkArchiver':
            print("I'm gonna follow {}.".format(data['source']['screen_name']))
            twitter_follow(data['source']['screen_name'])
    else:
        print(data)

def log_failure(status_code, data):
    print("Something's gone terribly wrong: " + str(status_code) + " " + str(data))

def twitter_follow(screen_name):
    config = get_config()
    twitter = get_twitter_instance(config)
    try:
        twitter.create_friendship(screen_name=screen_name)
    except TwythonError as err:
        print("Had this error, bud: " + str(err))

def tweet_reply(archive_link, tweet_id, screen_name):
    config = get_config()
    twitter = get_twitter_instance(config)
    if archive_link:
        message = "Here's your archived link: " + archive_link
    else:
        message = "Sorry, something went wrong :("
    try:
        twitter.update_status(status = "@" + screen_name + " " + message,
                in_reply_to_status_id = tweet_id)
    except:
        pass

def grab_urls(tweet):
    url_list = []
    for url in tweet['entities']['urls']:
        if url['expanded_url']:
            print("Adding {} to the list of URLs to be archived.".format(url['expanded_url']))
            url_list.append(url['expanded_url'])
    return url_list

def send_to_archive(link):
    print("Sending {} to the Internet Archive.".format(link))
    if link:
        try:
            res = requests.get("https://web.archive.org/save/{}".format(link),
                    headers = {'user-agent':'@LinkArchiver twitter bot'})
            with open(os.path.join(fullpath,"log.txt"),"a") as f:
                f.write(link + "\n")
            return "https://web.archive.org" + res.headers['Content-Location']
        except:
            pass
def main():
    config = get_config()
    twitter = get_twitter_instance(config)
    streamer = get_stream_instance(config)

    streamer.on_success = check_tweet
    streamer.on_error = log_failure

    streamer.user(replies=all)

if __name__ == '__main__':
    main()
