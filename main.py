# let me know when ur here
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    km = value[value.index(",")+2:value.index("m")+1]
    km_filtered = "".join(filter(str.isdigit, km))
    km_num = int(km_filtered)
    return km_num

def get_Leistung(value):
    leistung = value[value.index("m")+3:]
    output_string = ''.join(filter(str.isalnum, leistung)).replace('\xa0', ' ')  
    return output_string[0:5] + " (" + output_string[5:] + ")" 
def get_Price(value):
    
    price_string = ''.join(filter(str.isdigit, value))
    priceNum = int(price_string)
    return priceNum
    
    
AutoInfo = {
    "Name": None,
    "Price": None,
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
    name = data.find_next('span', {'class': 'h3 u-text-break-word'})
    price = data.find_next('span', {'class': 'h3 u-block'})
    value = data.string
    if name or price is not None:
        print(name)
        print(price)
        print (value)

        AutoInfo["Name"] = name.string
        AutoInfo["Price"] = get_Price(price.string)
        AutoInfo["Kilometerstand"] = get_KilometerStand(value)
        AutoInfo["Erstzulassung"] = get_Erstzulassung(value)
        AutoInfo["Leistung"] = get_Leistung(value)

        Autoliste.append(AutoInfo)
    else:
        continue
      
    
   
   # print(name, price, value)
    #print()




print(Autoliste)

# test = "EZ 12/2020, 19.778 km, 180 kW (245 PS)"

# print(get_Erstzulassung(test))



# def find_nth(haystack, needle, n):
#     start = haystack.find(needle)
#     while start >= 0 and n > 1:
#         start = haystack.find(needle, start+len(needle))
#         n -= 1
#     return start