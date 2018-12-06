# -*- coding: utf-8 -*-
import random
import time
from pandas import read_json
import requests
import json
from clickhouse_driver import Client
from time import sleep

url1 = 'https://openexchangerates.org/api/latest.json?app_id=f68b28fcd4f642678f54e8725387778a'
df1 = read_json(url1, orient = 'rates')
dollar_rate = int(round(df1[df1.index=='RUB']['rates']))

url2 = 'http://api.openweathermap.org/data/2.5/weather?id=579464&APPID=7f87b9a7d651eadce7eba8355c144c55'
response = requests.get(url2)
data1 = json.loads(response.content)
percent_humidity = int(data1['main']['humidity'])

client = Client(host='localhost', port = '9000', database = 'metrika')
sql = 'select count(distinct(article_id)) from (select replaceAll(Params, \'""\', \'"\') as Params2, visitParamExtractInt(Params2, \'article_id\') as article_id, replaceAll(visitParamExtractRaw(Params2, \'published_date\'),\'"\',\'\') as published, Title from hits_all where Date = toDate(yesterday()) and published = toString(toDate(yesterday())) and match(URL, \'putin\')=1)'
count_putin_articles = int((client.execute(sql)[0])[0])

x = dollar_rate ** count_putin_articles % percent_humidity
y = x % 2

good_day = "Stepa is awesome"
bad_day = "Stepa is pidor"

if y == 1:
  message = bad_day
elif y == 0:
  message = good_day

#print(message)

url = "https://api.telegram.org/bot786285701:AAHBIxcV9COlJCeXbDCLPDHsNEAz8xGU2fg/"


def get_updates_json(request):  
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': message}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def main():  
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
           send_mess(get_chat_id(last_update(get_updates_json(url))), 'test')
           update_id += 1
    sleep(60)       
 
if __name__ == '__main__':  
    main()