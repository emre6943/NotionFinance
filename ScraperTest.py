
from FinanceApi import GetTradingView, GetCoinGeko


if __name__ == "__main__":
    # main
    # apple = GetStockInformation("https://www.tradingview.com/chart/?symbol=NASDAQ%3AAAPL")
    # print(apple)
    btc = GetTradingView("https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT")
    print(btc)

    gold = GetTradingView("https://www.tradingview.com/chart/?symbol=TVC-GOLD")
    print(gold)

    kara = GetTradingView("https://www.tradingview.com/chart/?symbol=BIST%3AKRDMA")
    print(kara)

    silver = GetTradingView("https://www.tradingview.com/chart/?symbol=TVC%3ASILVER")
    print(silver)

    eth = GetTradingView("https://www.tradingview.com/chart/?symbol=BINANCE%3AETHUSDT")
    print(eth)

    amk = GetTradingView("https://www.tradingview.com/chart/?symbol=NYSE%3AU")
    print(amk)

    tl = GetTradingView("https://www.tradingview.com/chart/?symbol=FX_IDC%3ATRYUSD")
    print(tl)
    print(GetCoinGeko("https://www.coingecko.com/en/coins/avalanche"))