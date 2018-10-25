from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import requests as re
import pandas as pn
import numpy as np
from bs4 import BeautifulSoup as lux
print("> Modules loaded")

consumer_key = "####"
consumer_secret = "####"
access_token = "####"
access_secret = "#####"

auth = OAuthHandler(consumer_key,consumer_secret)

auth.set_access_token(access_token,access_secret)

api = API(auth)

print("> Twitter API connection established")

feed = pn.read_csv('input.csv',engine='python')

fb_api = "https://graph.facebook.com/v3.1/"
page_id = "203823349640145_"
query_items = "/insights/post_impressions_unique,post_activity,post_video_views_unique?"
access_token = "access_token=#####"

print("> Facebook API credentials and query ready")

print("...")
print("PULLING DATA")
for ind,row in feed.iterrows():
    if('twitter' in row['link']):

        t_id = row['link'].split('/')[-1].strip()
        tweet = api.get_status(t_id)

        feed.loc[ind,'tw_retweets'] = tweet.retweet_count
        feed.loc[ind,'tw_favourites'] = tweet.favorite_count
        feed.loc[ind,'platform'] = 'twitter'
    
    elif('facebook' in row['link']):

        query_post = row['link'].split('/')[-1].strip()
        
        get_item = fb_api+page_id+query_post+query_items+access_token
        data = re.get(get_item).json()
        
        feed.loc[ind,'platform'] = 'facebook'
        feed.loc[ind,'fb_videoViews'] = data['data'][0]['values'][0]['value']
        feed.loc[ind,'fb_reach'] = data['data'][1]['values'][0]['value']
        feed.loc[ind,'fb_engagement'] = data['data'][2]['values'][0]['value']
    
    elif('youtu.be' in row['link']):
        
        page = re.get(row['link'])
        data = page.text
        soup = lux(data,'lxml')
        feed.loc[ind,'platform'] = 'youtube'
        feed.loc[ind,'yt_views'] = int(soup.find('div',{'class':'watch-view-count'})
                                       .text.split(" ")[0].replace(",",""))
        feed.loc[ind,'yt_likes'] = int(soup.find('button',{'class':'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip'})
            .text.split(" ")[0].replace(",",""))
        feed.loc[ind,'yt_dislikes'] = int(soup.find('button',{'class':'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip'})
            .text.split(" ")[0].replace(",",""))
    
    print("> Added metrics for: "+ row['link'])
print("...")
print("DONE")

feed.to_csv('output.csv',index=False)
print("> Data saved to 'output.csv'")