from cmath import exp
import requests
import warnings
from datetime import datetime as d
from requests_html import HTMLSession
import sys
from decouple import config
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from Helper import CoinMarketCapChanger, ConvertTextToNumber, FixPercatage, FixPercatageCoin, PrintDetail

def OpenBrowser(url):
    opt = webdriver.ChromeOptions()
    opt.add_argument("--headless")
    opt.add_argument("--no-sandbox")
    # open the browser
    browser = webdriver.Chrome("C:\\Users\\fbemr\\OneDrive\\Masaüstü\\Code\\chromedriver", chrome_options=opt)
    browser.get(url)
    browser.implicitly_wait(7)
    browser.maximize_window()
    # just wait a little for the website to load
    time.sleep(2)
    return browser

def GetTradingView(url):
    try:
        browser = OpenBrowser(url)

        # set default values incase if a value is not found
        price = None

        # read the price
        price = browser.find_element(By.CLASS_NAME, "priceWrapper-hSPni_lj").text
        browser.quit()

        if price[0] == '−':
            price = price[1:]

        # price
        return float(price.split('\n')[0])
    except Exception as e:
        print("ERROR : " + str(e))
        return -1

def GetCoinGeko(url):
    try:
        session = HTMLSession()
        r = session.get(url)

        price = r.html.search_all('${}.{}')[0][0]
        cent = r.html.search_all('${}.{}')[0][1]

        session.close()

        return float(f"{price}.{cent}")
    except:
        return -1
