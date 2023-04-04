# let me know when ur here
import requests
from bs4 import BeautifulSoup

with open('C:\\Users\\moham\\VSCode\\Auto.html', encoding='utf-8') as file:
    html = file.read()

# url = 'C:\Users\moham\VSCode\Auto.html'

# response = requests.get(url)
soup = BeautifulSoup(html, 'html.parser')
#Get Prices
# Auto_preislist = soup.find_all("span", {"class": "h3 u-block"})

# for preis in Auto_preislist:
#     print(preis.text.strip())

# #Get Data
Autodata_list = soup.find_all('div', {'data-testid': 'regMilPow'})

# for data in Autodata_list:
#     print(data.text.strip())
def get_Erstzulassung(value):
    return value[3:value.index(",")]

def get_KilometerStand(value):
    return value[value.index(",")+2:value.index("m")+1]

def get_Leistung(value):
    return value[value.index("m")+3:]
def get_Price(value):
    if value != "skip":
        price_string = ''.join(filter(str.isdigit, value))
        priceNum = int(price_string)
        return priceNum
    else:
        pass
    
AutoInfo = {
    "Name": None,
    "Preis": None,
    "Kilometerstand":"helo", 
    "Erstzulassung":"",
    "Leistung":""
}

Autoliste = []    


# test = '<span class="h3 u-block">48.750 €</span>'
# print(get_Price(test)-300000)
#Get Titel
for data in Autodata_list:
    #if type(data) == 
    # print(type)
    name = str(data.find_next('span', {'class': 'h3 u-text-break-word'}))
    price = data.find_next(class: 'h3 u-block')
    price_desc = price.getText() if price else "skip"
    print(price)
    
    
    value = data.text.strip()

    AutoInfo["Name"] = name
    AutoInfo["Price"] = get_Price(price_desc)
    AutoInfo["Kilometerstand"] = get_KilometerStand(value)
    AutoInfo["Erstzulassung"] = get_Erstzulassung(value)
    AutoInfo["Leistung"] = get_Leistung(value)

    Autoliste.append(AutoInfo)
   # print(name, price, value)
    #print()




print(Autoliste)

test = "EZ 12/2020, 19.778 km, 180 kW (245 PS)"

# print(get_Erstzulassung(test))



# def find_nth(haystack, needle, n):
#     start = haystack.find(needle)
#     while start >= 0 and n > 1:
#         start = haystack.find(needle, start+len(needle))
#         n -= 1
#     return start