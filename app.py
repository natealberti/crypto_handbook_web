from flask import Flask, render_template, request
import requests
import json
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import time
from io import BytesIO
import base64

app = Flask(__name__)

#connection to the API, returns data in json
def get_json(coin):
    endpoint = f'https://api.coingecko.com/api/v3/coins/{coin}'
    req = requests.get(endpoint)
    return json.loads(req.text)

#connection to API, returns last day of prices
def get_prices(coin):
    current = time.time()
    prev = current - 86400
    endpoint = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range?vs_currency=usd&from={prev}&to={current}'
    req = requests.get(endpoint)
    prices = []
    raw = json.loads(req.text)['prices']
    for i in raw:
        prices.append(i[1])
    return prices

#returns plot url for graph to pass to html
def get_plot_url(x, y):
    img = BytesIO()
    plt.plot(x, y)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

###home page
@app.route('/')
def homepage():
    #getting images for the links
    btc_img = get_json('bitcoin')['image']['small']
    eth_img = get_json('ethereum')['image']['small']
    usdt_img = get_json('tether')['image']['small']
    xrp_img = get_json('ripple')['image']['small']
    ltc_img = get_json('litecoin')['image']['small']
    #getting current prices
    btc_price = get_json('bitcoin')['market_data']['current_price']['usd']
    eth_price = get_json('ethereum')['market_data']['current_price']['usd']
    usdt_price = get_json('tether')['market_data']['current_price']['usd']
    xrp_price = get_json('ripple')['market_data']['current_price']['usd']
    ltc_price = get_json('litecoin')['market_data']['current_price']['usd']
    return render_template('homepage.html',
                           btc_img=btc_img,
                           eth_img=eth_img,
                           usdt_img=usdt_img,
                           xrp_img=xrp_img,
                           ltc_img=ltc_img,
                           btc_price='${:,.2f}'.format(btc_price),
                           eth_price='${:,.2f}'.format(eth_price),
                           usdt_price='${:,.2f}'.format(usdt_price),
                           xrp_price='${:,.2f}'.format(xrp_price),
                           ltc_price='${:,.2f}'.format(ltc_price),)

##bitcoin page
@app.route('/bitcoin')
def btc():
    #getting api response for btc
    j = get_json('bitcoin')
    #scraping the variables from the api response
    symbol = j['symbol']
    price = j['market_data']['current_price']['usd']
    desc = j['description']['en']
    image = j['image']['large']
    inception_date = j['genesis_date']
    market_cap = j['market_data']['market_cap']['usd']
    cap_rank = j['market_data']['market_cap_rank']
    daily_return = j['market_data']['market_cap_change_percentage_24h']
    in_circulation = j['market_data']['circulating_supply']
    total_circulation = j['market_data']['total_supply']
    website = j['links']['homepage'][0]
    try:
        pcent_in_circulation = 100*in_circulation/total_circulation
    except TypeError:
        pcent_in_circulation = 100
    #if daily return is neg/pos
    color = 'green'
    if(daily_return < 0):
        color = 'red'
    #putting plot into form for hmtl
    list = get_prices('bitcoin')
    length = []
    for i in range (len(list)):
        length.append(i)
    plot_url = get_plot_url(length, list)
    #redirecting user to bitcoin template
    return render_template('bitcoin.html',
                           symbol=str(symbol).upper(),
                           price='${:,.2f}'.format(price),
                           description=desc,
                           image=image,
                           inception_date=inception_date,
                           website=website,
                           market_cap='${:,}'.format(market_cap),
                           cap_rank=cap_rank,
                           daily_return='{:,.2f}'.format(daily_return)+'%',
                           color=color,
                           plot_url=plot_url,
                           pcent_in_circulation='{:,.2f}'.format(pcent_in_circulation)+'%')

##ethereum page
@app.route('/ethereum')
def eth():
    #getting api response for eth
    j = get_json('ethereum')
    #scraping the variables from the api response
    symbol = j['symbol']
    price = j['market_data']['current_price']['usd']
    desc = j['description']['en']
    image = j['image']['large']
    inception_date = j['genesis_date']
    market_cap = j['market_data']['market_cap']['usd']
    cap_rank = j['market_data']['market_cap_rank']
    daily_return = j['market_data']['market_cap_change_percentage_24h']
    in_circulation = j['market_data']['circulating_supply']
    total_circulation = j['market_data']['total_supply']
    website = j['links']['homepage'][0]
    try:
        pcent_in_circulation = 100*in_circulation/total_circulation
    except TypeError:
        pcent_in_circulation = 'n/a'
    #if daily return is neg/pos
    color = 'green'
    if(daily_return < 0):
        color = 'red'
    #putting plot into form for hmtl
    list = get_prices('ethereum')
    length = []
    for i in range (len(list)):
        length.append(i)
    plot_url = get_plot_url(length, list)
    #redirecting user to ethereum template
    return render_template('ethereum.html',
                           symbol=str(symbol).upper(),
                           price='${:,.2f}'.format(price),
                           description=desc,
                           image=image,
                           inception_date=inception_date,
                           website=website,
                           market_cap='${:,}'.format(market_cap),
                           cap_rank=cap_rank,
                           daily_return='{:,.2f}'.format(daily_return)+'%',
                           color=color,
                           plot_url=plot_url,
                           pcent_in_circulation=pcent_in_circulation)

##tether page
@app.route('/tether')
def usdt():
    #getting api response for usdt
    j = get_json('tether')
    #scraping the variables from the api response
    symbol = j['symbol']
    price = j['market_data']['current_price']['usd']
    desc = j['description']['en']
    image = j['image']['large']
    inception_date = j['genesis_date']
    market_cap = j['market_data']['market_cap']['usd']
    cap_rank = j['market_data']['market_cap_rank']
    daily_return = j['market_data']['market_cap_change_percentage_24h']
    in_circulation = j['market_data']['circulating_supply']
    total_circulation = j['market_data']['total_supply']
    website = j['links']['homepage'][0]
    pcent_in_circulation = 100*in_circulation/total_circulation
    #if daily return is neg/pos
    color = 'green'
    if(daily_return < 0):
        color = 'red'
    #putting plot into form for hmtl
    list = get_prices('tether')
    length = []
    for i in range (len(list)):
        length.append(i)
    plot_url = get_plot_url(length, list)
    #redirecting user to tether template
    return render_template('tether.html',
                           symbol=str(symbol).upper(),
                           price='${:,.2f}'.format(price),
                           description=desc,
                           image=image,
                           inception_date=inception_date,
                           website=website,
                           market_cap='${:,}'.format(market_cap),
                           cap_rank=cap_rank,
                           daily_return='{:,.2f}'.format(daily_return)+'%',
                           color=color,
                           plot_url=plot_url,
                           pcent_in_circulation='{:,.2f}'.format(pcent_in_circulation)+'%')

##xrp page
@app.route('/xrp')
def xrp():
    #getting api response for usdt
    j = get_json('ripple')
    #scraping the variables from the api response
    price = j['market_data']['current_price']['usd']
    desc = j['description']['en']
    image = j['image']['large']
    inception_date = j['genesis_date']
    market_cap = j['market_data']['market_cap']['usd']
    cap_rank = j['market_data']['market_cap_rank']
    daily_return = j['market_data']['market_cap_change_percentage_24h']
    in_circulation = j['market_data']['circulating_supply']
    total_circulation = j['market_data']['total_supply']
    website = j['links']['homepage'][0]
    pcent_in_circulation = 100*in_circulation/total_circulation
    #if daily return is neg/pos
    color = 'green'
    if(daily_return < 0):
        color = 'red'
    #putting plot into form for hmtl
    list = get_prices('ripple')
    length = []
    for i in range (len(list)):
        length.append(i)
    plot_url = get_plot_url(length, list)
    #redirecting user to tether template
    return render_template('xrp.html',
                           price='${:,.2f}'.format(price),
                           description=desc,
                           image=image,
                           inception_date=inception_date,
                           website=website,
                           market_cap='${:,}'.format(market_cap),
                           cap_rank=cap_rank,
                           daily_return='{:,.2f}'.format(daily_return)+'%',
                           color=color,
                           plot_url=plot_url,
                           pcent_in_circulation='{:,.2f}'.format(pcent_in_circulation)+'%')

##litecoin page
@app.route('/litecoin')
def ltc():
    #getting api response for usdt
    j = get_json('litecoin')
    #scraping the variables from the api response
    symbol = j['symbol']
    price = j['market_data']['current_price']['usd']
    desc = j['description']['en']
    image = j['image']['large']
    inception_date = j['genesis_date']
    market_cap = j['market_data']['market_cap']['usd']
    cap_rank = j['market_data']['market_cap_rank']
    daily_return = j['market_data']['market_cap_change_percentage_24h']
    in_circulation = j['market_data']['circulating_supply']
    total_circulation = j['market_data']['total_supply']
    website = j['links']['homepage'][0]
    pcent_in_circulation = 100*in_circulation/total_circulation
    #if daily return is neg/pos
    color = 'green'
    if(daily_return < 0):
        color = 'red'
    #putting plot into form for hmtl
    list = get_prices('litecoin')
    length = []
    for i in range (len(list)):
        length.append(i)
    plot_url = get_plot_url(length, list)
    #redirecting user to tether template
    return render_template('litecoin.html',
                           symbol=str(symbol).upper(),
                           price='${:,.2f}'.format(price),
                           description=desc,
                           image=image,
                           inception_date=inception_date,
                           website=website,
                           market_cap='${:,}'.format(market_cap),
                           cap_rank=cap_rank,
                           daily_return='{:,.2f}'.format(daily_return)+'%',
                           color=color,
                           plot_url=plot_url,
                           pcent_in_circulation='{:,.2f}'.format(pcent_in_circulation)+'%')

if __name__ == '__main__':
    print(len(get_prices('bitcoin')))