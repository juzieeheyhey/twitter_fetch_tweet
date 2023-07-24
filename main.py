import tweepy
import time
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

def api():
    api = tweepy.Client(bearer_token=bearer_token,
                         consumer_key=api_key,
                         consumer_secret=api_key_secret,
                         access_token=access_token,
                         access_token_secret=access_token_secret)
    return api

def tweet(api: tweepy.Client, message: str):
    api.create_tweet(text=message)
    print("Tweeted successfully!")


''' Fetch data from Boston University'''
def fetch_bu():
    url = 'https://www.bu.edu/admissions/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')

    stats = soup.find_all('div', class_= 'bu-infographics')
    for stat in stats:
        colorStudent = stat.find('div', class_='donut-chart')['data-percent-final']
        firstgen = stat.find('div', class_= 'bu-infographic-number aqua col-md-6').span.text
        howard = stat.find('div', class_='bu-infographic-accent-statistic black col-md-6').span.text
        pellgrant = stat.find('div', class_= 'bu-infographic-number red col-md-6').span.text
        message = f'''
                {colorStudent}% of enrolled domestic students are students of color
            {firstgen} are first-generation college students
            {howard} meetings and events hosted by the Howard Thurman Center for Common Ground
            {pellgrant} of enrolled students are Pell-Grant recipients
            '''
    return message


    
if __name__ == '__main__':
    api = api()
    message = fetch_bu()
    tweet(api, message)
    