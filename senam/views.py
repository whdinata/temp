import requests
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from alchemyapi import AlchemyAPI
from parse_rest.connection import register
from parse_rest.datatypes import Object

class Sentiment(Object):
    pass
# Create your views here.

def index(request):
    application_id = "gi2pYK4VspR1wawE8gxHH1w7qLvwVZhzmF0zmn2t"
    rest_api_key = "ylVljCcxgDhFtpJBIYcuVu0pl2mydsFTmCH3OHSN"
    master_key = "Ixe4yNMRIbxeVUBtm4eVgVSVfG1qOnIviOmgFUI6"

    register(application_id, rest_api_key)
    places = ['%22calton%20hill%22', '%22arthur%20seat%22', 'Portobello%20Beach', '%22Princes%20Street%22']
    #places = ['%22Princes%20Street%22'] 
    placeIds = ['ch', 'as', 'pb', 'ps']

    headers = {'Host' : 'api.twitter.com', 
                'User-Agent' : 'Senam',
    #            'Authorization' : 'Basic eTJsemZDQUQxUWtndXVob2dMb0U3VXEydjpIUml2ZTB3c1JsWGFyMkdaNVQySWFqQndjbmNNMk84UFVnSFk5TEkxQ25NTjVVWUo2Rw==',
                'Authorization' : 'Bearer AAAAAAAAAAAAAAAAAAAAAL5JuAAAAAAAu8i%2FzxYsLvliCp7p3FXhyP80Wug%3DJ9YZzPWMDWsPiE3kro7pv0GwJc5PPtmDJDpPFPsMmclsHuy18K',
    #            'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8',
    #            'Content-Length' : '29',
                'Accept-Encoding' : 'gzip'}

    r = requests.post('https://api.twitter.com/oauth2/token', data={'grant_type' : 'client_credentials'}, headers=headers) 
    result = '';

    total = 0
    placeIndex = -1

    for place in places:
        date = 26
        placeIndex = placeIndex + 1
        while (date >= 1):
            if date < 10:
                dateStr = '0' + str(date)
            else:
                dateStr = str(date)

            r = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=' + place + "%20until%3A2016-04-" + dateStr + "&count=100", headers=headers)
            jsonData = r.json()
            statuses = jsonData['statuses']
     
            result = result + "Place: " + place + '<br />' + "Number of statuses: " + str(len(statuses)) + '<br />'; 
            result = result + "Query string: " + str(date) + "<br />" 
            total += len(statuses)

            if len(statuses) == 0:
                break
            
            for status in statuses: 
                timePosted = status['created_at']
                text = status['text']

                response = getSentiment(text)

                if response.has_key('docSentiment'):
                    if len(response['docSentiment']) > 1:
                        score = response['docSentiment']['score']
                    else:
                        score = '0'

                    sentiment = Sentiment(place=placeIds[placeIndex], status=text, sentimentScore=score, sentimentType=response['docSentiment']['type'], tweetTime=timePosted)
                #sentiment = Sentiment(place=placeIds[placeIndex], status=text)
                    sentiment.save()
   
                break 
                    #result = result + response['docSentiment']['score'] + '<br />'
                result = result + "Status: " + text + '<br />' + "Created At: " + timePosted + '<br />'
                date = timePosted[8:10]

            break

            result += '<br />';
        #result = result + 'text: ' + text + '<br />' + 'sentiment: ' + sentiment
        break
 
    return HttpResponse(response['statusInfo'])

def getSentiment(text):
    alchemyapi = AlchemyAPI()
    response = alchemyapi.sentiment("text", text)
    return response


