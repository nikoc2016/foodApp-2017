from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from foodApp.forms import *
from django.contrib.staticfiles import *
import json
from django.http import JsonResponse
import json
from pprint import pprint
import http.client, urllib.parse, json
import string
from random import randint
import tweepy
import operator

# ========================================================================================
# Function that render the web page
def index(request):
    return render(request, 'foodApp/index.html')

# ========================================================================================
# Function that communicate with client side
# Input: clicked state's code on web page
# Output: JSON file
def communicate(request):
    stateClicked = request.GET.get('clickedState', None)
    feedback = director(stateClicked)
    return JsonResponse(feedback)

# ========================================================================================
# Supreme Function that handles everything
# Input: state code
# Output: the final json
def director(stateCode):
    stateName = codeToStatename(stateCode)
    tweets = tweepySearch(stateName)
    frequencyTable = foodCounter(tweets)
    return packJson(frequencyTable, stateName)

# ========================================================================================
# The function coverts state code to state name
# Input: state code
# Output: state name
def codeToStatename(stateCode):
    stateDictionary = json.loads(open("foodApp/states_hash.json").read())
    return stateDictionary[stateCode]

# ========================================================================================
# The function that build a frequency table for the tweets
# Input: tweets
# Output: frequency table
def foodCounter(tweets):
    with open('foodApp/foodlist.txt') as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    freqTable = {}
    for food in content:
        freqTable[food] = 0
    for tweet in tweets:
        for food in freqTable:
            freqTable[food] += tweet.count(food)
            # print('looking for ' + food + ' in ' + tweet )

    freqTable = sorted(freqTable.items(), key=operator.itemgetter(1), reverse = True)
    print("Frequency table:")
    print(freqTable)
    return freqTable

# ========================================================================================
# The function pack all response to JSON file
# Input: frequency table, state name
# Output: a packed JSON
def packJson(table,stateName):
    foodName = []
    foodURLs = []

    i = 0
    for food in table:
        if i < 3:
            foodName.append(food[0])
        i += 1

    for food in foodName:
        searchText = food
        print('Searching images for: ', searchText)
        headers, result = BingImageSearch(searchText)
        picPtr = randint(0, 9)
        foodURLs.append(json.loads(result)["value"][picPtr]["contentUrl"])

    feedback = {
        'valid': 'true',
        'output': 'Server Response: You clicked ' + stateName,
        'picUrl1': foodURLs[0],
        'picUrl2': foodURLs[1],
        'picUrl3': foodURLs[2],
        'picInfo': 'The top 3 foods of ' + stateName + " are:</br><h1>1." + foodName[0] + "</br></br>2." + foodName[1] + "</br></br>3." + foodName[2] + "</h1>",
    }

    print('JSON back : ', feedback)
    return feedback

# ========================================================================================
# Function that simulates the tweet API
# Use this function when API runs out of usage
def virtualTweepySearch(search_string):
    print('Virtual Tweepy Activated! All twitters are simulated')
    virtualTweets = []
    virtualTweets.append("pizza pizza pizza")
    virtualTweets.append("cheese cheese")
    virtualTweets.append("steak")
    return virtualTweets


# ========================================================================================
# Function which emulates the real process
def virtualDirector(stateCode):
    print('Director Simulator Activated!')
    stateDictionary = json.loads(open("foodApp/states_hash.json").read())
    stateName = stateDictionary[stateCode]
    searchText = stateName + " food"

    print('Searching images for: ', searchText)
    headers, result = BingImageSearch(searchText)

    infoPtr = randint(0,9)
    feedback = {
        'valid':'true',
        'output': 'Server Response: You clicked ' + stateName,
        'picUrl': json.loads(result)["value"][infoPtr]["contentUrl"],
        'picInfo': json.loads(result)["value"][infoPtr]["name"],
    }

    return feedback

# ========================================================================================
# Tweet Search API
def tweepySearch(search_string):
    tweets = []
    my_consumer_key = 'xDPUrwZYvozXscpnNG3qvk920'
    my_consumer_secret = 'tgmHJQV3CFfcStMDDRZf3HS6hZTzeMyBbLCX6tUX38k92mlbh2'
    my_access_token_key = '94859656-Mc4VYbWTahd2Jl7NpYNmnIH5ISBM0PPgHEPKLDgAi'
    my_access_token_secret = 'Wgwcb3mHw0vHY9Tccnbqu56SZkC9Flq9SFlQZtTRfu9xv'
    auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret)
    auth.set_access_token(my_access_token_key, my_access_token_secret)

    api = tweepy.API(auth)
    places = api.geo_search(query=search_string)
    place_id = places[0].id
    print(places)
    cricTweet = tweepy.Cursor(api.search, q="place:" + place_id + "food OR BBQ").items(500)
    for tweet in cricTweet:
        tweets.append(tweet.text)
    print('There are ' + str(len(tweets)) + ' tweets returned.')
    return tweets

# ========================================================================================
# Bing Image Search Function
subscriptionKey = "f36d2c0361364d55ae34e20f22ee808a"
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/images/search"
term = "puppies"


def BingImageSearch(search):
    "Performs a Bing image search and returns the results."
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")