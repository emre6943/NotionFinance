# imports
import requests
import json
from datetime import datetime
from decouple import config
import time

from FinanceApi import GetCoinInformation, GetCryptoInformation, GetStockInformation
from Helper import PrintDetail

# env vars
token = config('SECRET_TOKEN')
databaseId = config('DATABASE_ID')
# base currecy Ids
TL = config('TL')
EUR = config('EUR')

# make sure to get the most recent notion version
notionVersion = "2021-08-16"

databaseUrl = f"https://api.notion.com/v1"
headers = {
    "Authorization" : "Bearer " + token,
    "Content-Type" : "application/json",
    "Notion-Version" : notionVersion
}

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
PrintDetail("START", "RUNING TIME", now)


def ChangeValuesAcordingToBaseCurrecy(base, arr):
    if (base == "USD"):
        return arr

    if (base == "EUR"):
        PrintDetail("LOG", "EURO FOUND", arr)

        getUrl = f"{databaseUrl}/pages/{EUR}"
        res = requests.request("GET", getUrl, headers=headers)
        euro = res.json()["properties"]["Price"]["number"]

        arr[0] = arr[0] * euro
        return arr

    if (base == "TL"):
        PrintDetail("LOG", "TL FOUND", arr)

        getUrl = f"{databaseUrl}/pages/{TL}"
        res = requests.request("GET", getUrl, headers=headers)
        tl = res.json()["properties"]["Price"]["number"]

        arr[0] = arr[0] * tl
        return arr
        
    PrintDetail("ERROR", "FOUND AN UKNOWN BASE CURRENCY", base)
    return arr
    


def UpdatePage(pageId, arr):
    # arr will have the values in this order
    # price, pe, dividence, marketCap, 1week, 1month, 3months
    updateUrl = f"{databaseUrl}/pages/{pageId}"

    updateData = {
        "properties" : {
            "Price" : {
                "number" : arr[0]
            },
            "P/E Ratio" : {
                "number" : arr[1]
            },
            "Dividence" : {
                "number" : arr[2]
            },
            "1 Week" : {
                "number" : arr[4]
            },
            "1 Month" : {
                "number" : arr[5]
            },
            "3 Months" : {
                "number" : arr[6]
            },
            "Market Cap": {
                "rich_text": [
                    {
                        "text" : {
                            "content" : arr[3]
                        }
                    }
                ]
            },
            "API Updated": {
                "rich_text": [
                    {
                        "text" : {
                            "content" : now
                        }
                    }
                ]
            }
        }
    }
    data = json.dumps(updateData)

    res = requests.request("PATCH", updateUrl, headers=headers, data=data)
    PrintDetail("LOG", "UPDATE STATUS", res.status_code)
    if (res.status_code != 200):
        PrintDetail("ERROR", "UPDATE CONTENT", res.content)


def IterateAndUpdateDatabase():
    readUrl = f"{databaseUrl}/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    PrintDetail("LOG", "READ DATABASE STATUS", res.status_code)
    data = res.json()

    # saving
    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

    for page in data["results"]:
        id = page['id']
        url = page['properties']['URL']['url']

        if (url != None and len(url) > 5):
            PrintDetail("LOG", "UPDATING", page['properties']['Name']['title'][0]['plain_text'])
            if (url.split("/")[2] == 'www.coingecko.com'):
                arr = GetCoinInformation(url)
                arr = ChangeValuesAcordingToBaseCurrecy(page['properties']['Base Currency']['select']['name'], arr)
                PrintDetail("LOG", "SCRAPED COINGECKO DETAILS", arr)
                UpdatePage(id, arr)
            elif (page['properties']['Type']['multi_select'][0]['name'] == 'Crypto'):
                arr = GetCryptoInformation(url)
                arr = ChangeValuesAcordingToBaseCurrecy(page['properties']['Base Currency']['select']['name'], arr)
                PrintDetail("LOG", "SCRAPED CRYPTO DETAILS", arr)
                UpdatePage(id, arr)
            elif (page['properties']['Type']['multi_select'][0]['name'] == 'Money'):
                arr = GetCryptoInformation(url)
                arr = ChangeValuesAcordingToBaseCurrecy(page['properties']['Base Currency']['select']['name'], arr)
                PrintDetail("LOG", "SCRAPED FOREX DETAILS", arr)
                UpdatePage(id, arr)
            else:
                arr = GetStockInformation(url)
                arr = ChangeValuesAcordingToBaseCurrecy(page['properties']['Base Currency']['select']['name'], arr)
                PrintDetail("LOG", "SCRAPED STOCK DETAILS", arr)
                UpdatePage(id, arr)


if __name__ == "__main__":
    # main
    start_time = time.time()
    print(f"STARTING TO UPDATE , {start_time}")
    IterateAndUpdateDatabase()
    print(f"DONE, {time.time() - start_time}")