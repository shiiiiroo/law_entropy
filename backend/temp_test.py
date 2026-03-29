import requests
import bs4
import urllib3
import urllib.parse
urllib3.disable_warnings()

query = "налог"
url = f"https://adilet.zan.kz/rus/search/docs?fulltext={urllib.parse.quote_plus(query)}"
resp = requests.get(url, verify=False)
soup = bs4.BeautifulSoup(resp.text, 'lxml')

results = soup.find_all(lambda tag: tag.name == 'a' and tag.has_attr('href') and '/rus/docs/' in tag['href'] and not 'search' in tag['href'])
seen = []
for a in results:
    if a.get_text(strip=True) and a.get_text(strip=True) not in seen:
        seen.append(a.get_text(strip=True))
        
print("Found unique documents:", len(seen))
for text in seen[:5]:
    print(" -", text[:50])
