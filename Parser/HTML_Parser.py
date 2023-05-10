import requests
from bs4 import BeautifulSoup

# URL of the LinkedIn article
url = 'https://de.indeed.com/Jobs?l=langenfeld&radius=0&sort=date&vjk=478c627e142c261b'
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64"
           }

response = requests.get(url, headers=headers)

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(response.content, 'lxml')
jobs_list = soup.find("ul", class_ ="jobsearch-ResultsList css-0")
print(soup)






