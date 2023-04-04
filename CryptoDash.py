###########################################
#             Les librairies              #
###########################################
import requests, sqlite3
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd 
###########################################
#             Base de données             #
###########################################
filename = "crypto.db"
path = 'E:\Projet Fil Rouge\crypto.db'
conn = sqlite3.connect(path)
c = conn.cursor()
###########################################
#             Fonction Temps              #
###########################################
Temps = datetime.now()
n = 2
Temps_changé = Temps - pd.DateOffset(hours=n)
Temps_changé_str = Temps_changé.strftime('%Y-%m-%d %H:%M:%S')
###########################################
#             Fonction Crypto             #
###########################################
def crypto(url):
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    #Monnaie
    monnaie = soup.find("h1",{"CoinPageHead__Symbol"}).text.replace('<h1 class="CoinPageHe ad__Symbol">', "")
    #Pourcentage
    pourcentage = soup.find("div",{"CoinPageHead__PriceChange"}).text.replace('<div class="CoinPageHead__PriceChange">', "")
    stringPourcentage = pourcentage
    characters = "(%)"
    stringPourcentage = ''.join( x for x in stringPourcentage if x not in characters)
    #Prix
    prix = soup.find("div",{"CoinPageHead__PriceUsd"}).text.replace('<div class="CoinPageHead__PriceUsd">', "")
    stringPrix = prix
    characters = ",","$"
    stringPrix = ''.join( x for x in stringPrix if x not in characters)
    pourcentage = soup.find("div",{"CoinPageHead__PriceChange"}).text.replace('<div class="CoinPageHead__PriceChange">', "")
    #Rang
    rang = soup.find("span",{"ExtraInfoBlock__MarketcapRank"}).text.replace('<span class="ExtraInfoBlock__MarketcapRank">', "")
    stringRang = rang
    characters = "#"
    stringRang = ''.join( x for x in stringRang if x not in characters)
    #Prix
    volume = soup.find("div",{"CoinPageHead__InfoBlockValue"}).text.replace('<div class="CoinPageHead__InfoBlockValue">', "")
    stringVolume = volume
    characters = ",","$"
    stringVolume = ''.join( x for x in stringVolume if x not in characters)
    #BTC
    BTC = soup.find("div",{"CoinPageHead__PriceBtc"}).text.replace('<div class="CoinPageHead__PriceBtc">', "")
    stringBTC = BTC
    characters = "BTCSA"
    stringBTC = ''.join( x for x in stringBTC if x not in characters)
    #c.execute('''CREATE TABLE ['''+monnaie+'''](rang STR, monnaie STR, prix STR, date DATE, BTC STR, pourcentage STR, volume STR)''')
    c.execute('''INSERT INTO ['''+monnaie+'''] VALUES(?,?,?,?,?,?,?)''', (stringRang, monnaie, stringPrix, Temps_changé_str, stringBTC, stringPourcentage, stringVolume))
    c.execute('''SELECT * FROM ['''+monnaie+''']''')
###########################################
#               Les cryptos               #
###########################################
crypto('https://coin360.com/coin/ethereum-eth')
crypto('https://coin360.com/coin/bitcoin-btc')
crypto('https://coin360.com/coin/binance-coin-bnb')
crypto('https://coin360.com/coin/tether-usdt')
crypto('https://coin360.com/coin/cardano-ada')
crypto('https://coin360.com/coin/solana-sol')
crypto('https://coin360.com/coin/ripple-xrp')
crypto('https://coin360.com/coin/polkadot-dot')
crypto('https://coin360.com/coin/shiba-inu-shib')
crypto('https://coin360.com/coin/usd-coin-usdc')
###########################################
#            Fermeture de la DB           #
###########################################
conn.commit()
conn.close()

