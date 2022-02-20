def PrintDetail(type, message, variable):
    print(f"<{type}> {message}: {variable}")

def FixPercatage(percentText):
    if (len(percentText) == 0 or percentText == '' or percentText == '—'):
        return None
    elif (percentText[0] == '−'):
        return round(float(percentText[1:-1])/100 * -1, 3)
    else:
        return round(float(percentText[:-1])/100, 3)

def FixPercatageCoin(percentText):
    if (len(percentText) == 0 or percentText == '' or percentText == '-'):
        return None
    elif (percentText[0] == '-'):
        return round(float(percentText[1:-1])/100 * -1, 3)
    else:
        return round(float(percentText[:-1])/100, 3)

def ConvertTextToNumber(text):
    if (len(text) == 0 or text == '' or text == '—'):
        return None

    text = text.replace(',', '')

    if (text[0] == '−'):
        return round(float(text[1:]) * -1, 3)
    elif (text[0] == '$'):
        return round(float(text[1:]), 3)
    else:
        return round(float(text), 3)

def CoinMarketCapChanger(text):
    clean = text[1:]
    clean = clean.split(',')
    if (len(clean) == 3):
        return f"{clean[0]}.{clean[1]}M"
    elif (len(clean) == 4):
        return f"{clean[0]}.{clean[1]}B"
    elif (len(clean) == 5):
        return f"{clean[0]}.{clean[1]}T"
    else:
        return f"WTF{text}"