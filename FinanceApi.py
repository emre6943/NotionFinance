from cmath import exp
from selenium import webdriver
import time
import warnings
warnings.filterwarnings('ignore')

from Helper import CoinMarketCapChanger, ConvertTextToNumber, FixPercatage, FixPercatageCoin, PrintDetail

def OpenBrowser(url):
    opt = webdriver.ChromeOptions()
    opt.add_argument("--headless")
    opt.add_argument("--no-sandbox")
    # open the browser
    browser = webdriver.Chrome("location to/chromedriver_linux", chrome_options=opt)
    browser.get(url)
    browser.implicitly_wait(7)
    browser.maximize_window()
    # just wait a little for the website to load
    time.sleep(3)
    return browser

def TradingViewHistoryReader(url, browser, divclass, textclass, valueclass, week1, month1, month3):
    for elem in browser.find_elements_by_class_name(divclass):
            name = elem.find_element_by_class_name(textclass).text
            if (name == "1W"):
                try:
                    week1 = FixPercatage(elem.find_element_by_class_name(valueclass).text)
                except:
                    PrintDetail("ERROR", "COULDN'T READ 1 WEEK", url) 
            if (name == "1M"):
                try:
                    month1 = FixPercatage(elem.find_element_by_class_name(valueclass).text)
                except:
                    PrintDetail("ERROR", "COULDN'T READ 1 MONTH", url)
            if (name == "3M"):
                try:
                    month3 = FixPercatage(elem.find_element_by_class_name(valueclass).text)
                except:
                    PrintDetail("ERROR", "COULDN'T READ 3 MONTH", url)
    return week1, month1, month3

def GetStockInformation(url):
    browser = OpenBrowser(url)

    # set default values incase if a value is not found 
    price, pe, dividence, marketCap, week1, month1, month3 = None, None, None, 'NotFound', None, None, None

    # read the price
    try:
        price = ConvertTextToNumber(browser.find_element_by_class_name("price-3PT2D-PK").text)
    except:
        PrintDetail("ERROR", "COULDN'T FIND PRICE", url)

    # open the details
    try:
        button = browser.find_element_by_class_name("button-XCmieq1Q")
        button.click()
    except:
        PrintDetail("LOG", "NO BUTTON TO CLICK", None)

    # wait 1 secs
    time.sleep(1)

    # get the pe and dividence
    parentClass = "item-3iXCXbow"
    nameClass = "title-3iXCXbow"
    numberClass = "data-3iXCXbow"
    try:
        for elem in browser.find_elements_by_class_name(parentClass):
            name = elem.find_element_by_class_name(nameClass).text
            if (name == "DIVIDENDS YIELD (FY)"):
                try:
                    dividence = FixPercatage(elem.find_element_by_class_name(numberClass).text)
                except:
                    PrintDetail("ERROR", "COULDN'T READ DIVIDENCE", url) 
            if (name == "PRICE TO EARNINGS RATIO (TTM)"):
                try:
                    pe = ConvertTextToNumber(elem.find_element_by_class_name(numberClass).text)
                except:
                    PrintDetail("ERROR", "COULDN'T READ PE", url) 
            if (name == "MARKET CAPITALIZATION"):
                try:
                    marketCap = elem.find_element_by_class_name(numberClass).text 
                except:
                    PrintDetail("ERROR", "COULDN'T READ MARKETCAP", url)
    except:
        PrintDetail("ERROR", "COULDN'T READ STOCK DETAILS", url) 

    # get the compared percantages
    divclass = "container-2XSxT4Uw"
    textclass = "period-2XSxT4Uw"
    valueclass = "percentage-2XSxT4Uw"
    try:
        week1, month1, month3 = TradingViewHistoryReader(url, browser, divclass, textclass, valueclass, week1, month1, month3)
    except:
        PrintDetail("ERROR", "COULDN'T READ STOCK HISTORY", url) 

    browser.quit()

    # price, pe, dividence, marketCap, 1week, 1month, 3months 
    return [price, pe, dividence, marketCap, week1, month1, month3]

def GetCryptoInformation(url):
    browser = OpenBrowser(url)

    # set default values incase if a value is not found 
    price, pe, dividence, marketCap, week1, month1, month3 = None, None, None, 'NotFound', None, None, None

    # read the price
    price = ConvertTextToNumber(browser.find_element_by_class_name("price-3PT2D-PK").text)

    # get the compared percantages
    divclass = "container-2XSxT4Uw"
    textclass = "period-2XSxT4Uw"
    valueclass = "percentage-2XSxT4Uw"
    try:
        week1, month1, month3 = TradingViewHistoryReader(url, browser, divclass, textclass, valueclass, week1, month1, month3)
    except:
        PrintDetail("ERROR", "COULDN'T READ CRYPTO HISTORY", url) 

    browser.quit()

    # price, pe, dividence, marketCap, 1week, 1month, 3months 
    return [price, pe, dividence, marketCap, week1, month1, month3]


# this gets the information from coingecko link
def GetCoinInformation(url):
    browser = OpenBrowser(url)

    # set default values incase if a value is not found 
    price, pe, dividence, marketCap, week1, month1, month3 = None, None, None, 'NotFound', None, None, None

    # read the price
    try:
        for elem in browser.find_elements_by_class_name("tw-text-3xl"):
            price = ConvertTextToNumber(elem.find_element_by_class_name("no-wrap").text)
    except:
        PrintDetail("ERROR", "COULDN'T READ GECKO PRICE", url) 

    # read the marketcap
    m = 0
    try:
        for elem in browser.find_elements_by_class_name("no-wrap"):
            if (m == 3):
                marketCap = CoinMarketCapChanger(elem.text)
            m+=1
    except:
        PrintDetail("ERROR", "COULDN'T READ GECKO MARKETCAP", url) 

    # # scroll to the histories, not sure 
    # browser.execute_script("window.scrollTo(0,document.body.scrollHeight/3)")
    # time.sleep(1)

    # get the compared percantages
    # coin gecko code is not as nice
    maindiv = "my-4"
    i = 0
    try:
        for elem in browser.find_element_by_class_name(maindiv).find_elements_by_xpath("./*"):
            # the second one have the data we need
            if (i == 1):
                j = 0
                for valbox in elem.find_elements_by_xpath("./*"):
                    if (j == 2):
                        for span in valbox.find_elements_by_xpath("./*"): 
                            week1 = FixPercatageCoin(span.text)
                    if (j == 4):
                        for span in valbox.find_elements_by_xpath("./*"): 
                            month1 = FixPercatageCoin(span.text)
                    j+=1
            i+=1
    except:
        PrintDetail("ERROR", "COULDN'T READ GECKO HISTORY", url) 

    browser.quit()

    # price, pe, dividence, marketCap, 1week, 1month, 3months 
    return [price, pe, dividence, marketCap, week1, month1, month3]


# manual tests
# apple = GetStockInformation("https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL")
# print(apple)
# eth = GetCryptoInformation("https://www.tradingview.com/chart/?symbol=BINANCE%3AETHUSDT")
# print(eth)
# mm = GetCoinInformation("https://www.coingecko.com/en/coins/million")
# print(mm)
# tl = GetCryptoInformation("https://www.tradingview.com/chart/?symbol=FX_IDC%3ATRYUSD")
# print(tl)
