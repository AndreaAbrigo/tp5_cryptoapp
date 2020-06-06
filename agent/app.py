import os
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import pymongo
import requests
import urllib.request
import urllib.parse
import http.client
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import hashlib


app = Flask(__name__)

def connect_db():
    conexion = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
    return conexion

def seleccionarBaseDeDatos():
    conexion=connect_db()
    db = conexion.monedas
    return db

def obtenerMonedas():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '49004412-1e5f-496e-be2d-97654b8cba75',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return data

@app.route('/guardarMonedas')
def guardarMonedas():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    data=obtenerMonedas()
    for i in range(500):
        id=data['data'][i]['id']
        name=data['data'][i]['name']
        symbol=data['data'][i]['symbol']
        slug=data['data'][i]['slug']
        num_market_pairs=data['data'][i]['num_market_pairs']
        date_added=str(data['data'][i]['date_added'])
        tags=data['data'][i]['tags']
        max_supply=str(data['data'][i]['max_supply'])
        circulating_supply=str(data['data'][i]['circulating_supply'])
        total_supply=str(data['data'][i]['total_supply'])
        platform=data['data'][i]['platform']
        cmc_rank=data['data'][i]['cmc_rank']
        last_update=str(data['data'][i]['last_updated'])
        price=str(data['data'][i]['quote']['USD']['price'])
        volume_24h=str(data['data'][i]['quote']['USD']['volume_24h'])
        percent_change_1h=str(data['data'][i]['quote']['USD']['percent_change_1h'])
        percent_change_24h=str(data['data'][i]['quote']['USD']['percent_change_24h'])
        percent_change_7d=str(data['data'][i]['quote']['USD']['percent_change_7d'])
        market_cap=str(data['data'][i]['quote']['USD']['market_cap'])
        last_updated=str(data['data'][i]['quote']['USD']['last_updated'])
        collection.insert({"id":id, 
        "name":name,
        "symbol":symbol,
        "slug":slug, 
        "num_market_pairs":num_market_pairs,
        "data_added":date_added,
        "tags":tags,
        "max_supply":max_supply,
        "circulating_supply":circulating_supply,
        "total_supply":total_supply,
        "platform": platform,
        "cmc_rank": cmc_rank,
        "last_updated":last_updated,
        "price":price,
        "volume_24h":volume_24h,
        "percent_change_1h":percent_change_1h,
        "percent_change_24h":percent_change_24h,
        "percent_change_7d": percent_change_7d,
        "market_cap":market_cap,
        "last_updated": last_updated
        })
    return("Hecho")

@app.route('/listarMonedas')
def listarMonedas():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    resultado=collection.find()
    # for r in resultado:
    #     print( "Id: ", r['id'], 
    #     "Name: ", r['name'], 
    #     "Symbol", r['symbol'], 
    #     "Slug:", r['slug'], 
    #     "Num market pairs:", r['num_market_pairs'],
    #     "Date added:", r['data_added'],
    #     "Tags:", r['tags'],
    #     "Max supply:", r['max_supply'],
    #     "Circulating supply:", r['circulating_supply'],
    #     "Total supply:", r['total_supply'],
    #     "Platform:", r['platform'],
    #     "Cmc rank:", r['cmc_rank'],
    #     "Last updated:", r['last_updated'],
    #     "Price:", r['price'],
    #     "Volume 24h:", r['volume_24h'],
    #     "Percent change 1h:", r['percent_change_1h'],
    #     "Percent change 24h:", r['percent_change_24h'],
    #     "Percent change 7d:", r['percent_change_7d'],
    #     "Market cap:", r['market_cap'],
    #     "Last updated:", r['last_updated'])
    # return render_template('/mostrar.html',resultado=datos)
    return resultado

@app.route('/buscarMoneda/<name>')
def buscarMoneda(name=""):
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    resultado=collection.find({'name':name})
    return resultado
    # for r in resultado:
    #     print( "Id: ", r['id'], 
    #     "Name: ", r['name'], 
    #     "Symbol", r['symbol'], 
    #     "Slug:", r['slug'], 
    #     "Num market pairs:", r['num_market_pairs'],
    #     "Date added:", r['data_added'],
    #     "Tags:", r['tags'],
    #     "Max supply:", r['max_supply'],
    #     "Circulating supply:", r['circulating_supply'],
    #     "Total supply:", r['total_supply'],
    #     "Platform:", r['platform'],
    #     "Cmc rank:", r['cmc_rank'],
    #     "Last updated:", r['last_updated'],
    #     "Price:", r['price'],
    #     "Volume 24h:", r['volume_24h'],
    #     "Percent change 1h:", r['percent_change_1h'],
    #     "Percent change 24h:", r['percent_change_24h'],
    #     "Percent change 7d:", r['percent_change_7d'],
    #     "Market cap:", r['market_cap'],
    #     "Last updated:", r['last_updated'])
    
    
    
@app.route('/top5')
def top5():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    resultado=collection.find({'cmc_rank':{'$lte':5}})
    return resultado

@app.route('/top20')
def top20():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    resultado=collection.find({'cmc_rank':{'$lte':20}})
    return resultado

@app.route('/eliminarMoneda/<name>') 
def eliminarMoneda(name=""):
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    resultado=collection.remove({'name':name})
    return "hecho"


@app.route('/almacenarDatosHasheados')
def almacenarDatosHasheados():
    conexion = MongoClient('localhost')
    db = seleccionarBaseDeDatos()
    collection = db.criptoMonedasHasheadas
    data=obtenerMonedas()
    for i in range(1):
        id=hashlib.sha256((str(data['data'][i]['id'])).encode('utf-8'))
        id=id.hexdigest()
        name=hashlib.sha256((str(data['data'][i]['name'])).encode('utf-8'))
        name=name.hexdigest()
        symbol=hashlib.sha256((str(data['data'][i]['symbol'])).encode('utf-8'))
        symbol=symbol.hexdigest()
        slug=hashlib.sha256((str(data['data'][i]['slug'])).encode('utf-8'))
        slug=slug.hexdigest()
        num_market_pairs=hashlib.sha256((str(data['data'][i]['num_market_pairs'])).encode('utf-8'))
        num_market_pairs=num_market_pairs.hexdigest()
        date_added=hashlib.sha256((str(data['data'][i]['date_added'])).encode('utf-8'))
        date_added=date_added.hexdigest()
        tags=hashlib.sha256((str(data['data'][i]['tags'])).encode('utf-8'))
        tags=tags.hexdigest()
        max_supply=hashlib.sha256((str(data['data'][i]['max_supply'])).encode('utf-8'))
        max_supply=max_supply.hexdigest()
        print("Antes de hashear", data['data'][i]['circulating_supply'], " del id ", data['data'][i]['id'])
        circulating_supply=hashlib.sha256((str(data['data'][i]['circulating_supply'])).encode('utf-8'))
        circulating_supply=circulating_supply.hexdigest()
        total_supply=hashlib.sha256((str(data['data'][i]['total_supply'])).encode('utf-8'))
        total_supply=total_supply.hexdigest()
        platform=hashlib.sha256((str(data['data'][i]['platform'])).encode('utf-8'))
        platform=platform.hexdigest()
        cmc_rank=data['data'][i]['cmc_rank']
        last_update=hashlib.sha256((str(data['data'][i]['last_updated'])).encode('utf-8'))
        last_update=last_update.hexdigest()
        price=hashlib.sha256((str(data['data'][i]['quote']['USD']['price'])).encode('utf-8'))
        price=price.hexdigest()
        volume_24h=hashlib.sha256((str(data['data'][i]['quote']['USD']['volume_24h'])).encode('utf-8'))
        volume_24h=volume_24h.hexdigest()
        percent_change_1h=hashlib.sha256((str(data['data'][i]['quote']['USD']['percent_change_1h'])).encode('utf-8'))
        percent_change_1h=percent_change_1h.hexdigest()
        percent_change_24h=hashlib.sha256((str(data['data'][i]['quote']['USD']['percent_change_24h'])).encode('utf-8'))
        percent_change_24h=percent_change_24h.hexdigest()
        percent_change_7d=hashlib.sha256((str(data['data'][i]['quote']['USD']['percent_change_7d'])).encode('utf-8'))
        percent_change_7d=percent_change_7d.hexdigest()
        market_cap=hashlib.sha256((str(data['data'][i]['quote']['USD']['market_cap'])).encode('utf-8'))
        market_cap=market_cap.hexdigest()
        last_updated=hashlib.sha256((str(data['data'][i]['quote']['USD']['last_updated'])).encode('utf-8'))
        last_updated=last_updated.hexdigest()
        collection.insert({"id":id, 
        "name":name,
        "symbol":symbol,
        "slug":slug, 
        "num_market_pairs":num_market_pairs,
        "data_added":date_added,
        "tags":tags,
        "max_supply":max_supply,
        "circulating_supply":circulating_supply,
        "total_supply":total_supply,
        "platform": platform,
        "cmc_rank": cmc_rank,
        "last_updated":last_updated,
        "price":price,
        "volume_24h":volume_24h,
        "percent_change_1h":percent_change_1h,
        "percent_change_24h":percent_change_24h,
        "percent_change_7d": percent_change_7d,
        "market_cap":market_cap,
        "last_updated": last_updated
        })
    return("Hecho")

@app.route('/listarMonedasHasheadas')
def listarMonedasHasheadas():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptoMonedasHasheadas
    resultado=collection.find()
    datos=[]
    print (datos)
    for r in resultado:
        print( "Id: ", r['id'], 
        "Name: ", r['name'],
        "Symbol", r['symbol'], 
        "Slug:", r['slug'], 
        "Num market pairs:", r['num_market_pairs'],
        "Date added:", r['data_added'],
        "Tags:", r['tags'],
        "Max supply:", r['max_supply'],
        "Circulating supply:", r['circulating_supply'],
        "Total supply:", r['total_supply'],
        "Platform:", r['platform'],
        "Cmc rank:", r['cmc_rank'],
        "Last updated:", r['last_updated'],
        "Price:", r['price'],
        "Volume 24h:", r['volume_24h'],
        "Percent change 1h:", r['percent_change_1h'],
        "Percent change 24h:", r['percent_change_24h'],
        "Percent change 7d:", r['percent_change_7d'],
        "Market cap:", r['market_cap'],
        "Last updated:", r['last_updated'])
    return "hecho"

@app.route('/chequearDatos/<rank>')
def chequearDatos(rank=""):
    bandera=True
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.criptomonedas
    moneda=collection.find({'cmc_rank':rank})
    for m in moneda:
        id=hashlib.sha256((str(m['id'])).encode('utf-8'))
        id=id.hexdigest()
        name=hashlib.sha256((str(m['name'])).encode('utf-8'))
        name=name.hexdigest()
        symbol=hashlib.sha256((str(m['symbol'])).encode('utf-8'))
        symbol=symbol.hexdigest()
        slug=hashlib.sha256((str(m['slug'])).encode('utf-8'))
        slug=slug.hexdigest()
        num_market_pairs=hashlib.sha256((str(m['num_market_pairs'])).encode('utf-8'))
        num_market_pairs=num_market_pairs.hexdigest()
        date_added=hashlib.sha256((str(m['data_added'])).encode('utf-8'))
        date_added=date_added.hexdigest()
        tags=hashlib.sha256((str(m['tags'])).encode('utf-8'))
        tags=tags.hexdigest()
        max_supply=hashlib.sha256((str(m['max_supply'])).encode('utf-8'))
        max_supply=max_supply.hexdigest()
        circulating_supply=hashlib.sha256((str(m['circulating_supply'])).encode('utf-8'))
        circulating_supply=circulating_supply.hexdigest()
        total_supply=hashlib.sha256((str(m['total_supply'])).encode('utf-8'))
        total_supply=total_supply.hexdigest()
        platform=hashlib.sha256((str(m['platform'])).encode('utf-8'))
        platform=platform.hexdigest()
        last_update=hashlib.sha256((str(m['last_updated'])).encode('utf-8'))
        last_update=last_update.hexdigest()
        price=hashlib.sha256((str(m['price'])).encode('utf-8'))
        price=price.hexdigest()
        volume_24h=hashlib.sha256((str(m['volume_24h'])).encode('utf-8'))
        volume_24h=volume_24h.hexdigest()
        percent_change_1h=hashlib.sha256((str(m['percent_change_1h'])).encode('utf-8'))
        percent_change_1h=percent_change_1h.hexdigest()
        percent_change_24h=hashlib.sha256((str(m['percent_change_24h'])).encode('utf-8'))
        percent_change_24h=percent_change_24h.hexdigest()
        percent_change_7d=hashlib.sha256((str(m['percent_change_7d'])).encode('utf-8'))
        percent_change_7d=percent_change_7d.hexdigest()
        market_cap=hashlib.sha256((str(m['market_cap'])).encode('utf-8'))
        market_cap=market_cap.hexdigest()
        last_updated=hashlib.sha256((str(m['last_updated'])).encode('utf-8'))
        last_updated=last_updated.hexdigest()
    cripto_hash = db.criptoMonedasHasheadas
    moneda_hash = cripto_hash.find({'cmc_rank':rank})
    for mh in moneda_hash:
        if (mh['id'] != id):
            bandera=False
        if (mh['name'] != name):
            bandera=False 
        if (mh['symbol'] != symbol):
            bandera=False
        if (mh['slug'] != slug):
            bandera=False
        if (mh['num_market_pairs'] != num_market_pairs):
            bandera=False 
        if (mh['data_added'] != date_added):
            bandera=False
        if (mh['tags'] != tags):
            bandera=False
        if (mh['max_supply'] != max_supply):
            bandera=False
        if (mh['circulating_supply'] != circulating_supply):
            bandera=False
        if (mh['total_supply'] != total_supply):
            bandera=False
        if (mh['platform'] != platform):
            bandera=False
        if (mh['last_updated'] != last_update):
            bandera=False
        if (mh['price'] != price):
            bandera=False
        if (mh['volume_24h'] != volume_24h):
            bandera=False
        if (mh['percent_change_1h'] != percent_change_1h):
            bandera=False
        if (mh['percent_change_24h']!= percent_change_24h):
            bandera=False
        if (mh['percent_change_7d'] != percent_change_7d):
            bandera=False
        if (mh['market_cap'] != market_cap):
            bandera=False
        if (mh['last_updated'] != last_update):
            bandera=False
    return bandera



if __name__ == '__main__':
    app.run(host='27017', port='5000', debug=False)
    