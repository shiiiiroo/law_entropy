import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib3
from typing import List, Dict, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdiletParser:
    BASE_URL = "http://adilet.zan.kz"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Search for documents by keyword on Adilet and return links.
        Note: Adilet search URL structure works via query parameters.
        """
        encoded_query = urllib.parse.quote_plus(query)
        # Assuming the search endpoint is /rus/search/docs
        # We will need to verify this or default to a known search param.
        # Often it's /rus/search/docs?query= or similar. 
        # For this prototype, if search is complex, we might just try to hit the search page or a known query.
        
        # In reality, their search form POSTs to /rus/search/docs
        # or uses ?fulltext=
        search_url = f"{self.BASE_URL}/rus/search/docs?fulltext={encoded_query}"
        
        try:
            response = self.session.get(search_url, timeout=15, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            results = []
            
            # Find the search results container. 
            # Needs actual DOM inspection, but let's guess typical classes initially:
            # Often it's a list or table of documents. Let's look for standard 'a' tags that link to /rus/docs/
            links = soup.find_all('a', href=True)
            for a in links:
                href = a['href']
                if '/rus/docs/' in href and not 'search' in href:
                    title = a.get_text(strip=True)
                    if title and title not in [r['title'] for r in results]:
                        full_url = self.BASE_URL + href if href.startswith('/') else href
                        results.append({
                            "title": title,
                            "url": full_url,
                            "source": "Әділет (adilet.zan.kz)"
                        })
                if len(results) >= limit:
                    break
                    
            return results
            
        except Exception as e:
            print(f"Error searching Adilet")
            return []

    def get_document_text(self, url: str) -> Optional[str]:
        """
        Fetch the full text of a specific legal document from Adilet.
        """
        try:
            response = self.session.get(url, timeout=15, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            # Extract content. Usually there's a specific div container, e.g., class="doc-content"
            # Without exact DOM, we'll try common containers or body text
            content_div = soup.find('div', class_='document') or soup.find('div', id='doc_content') or soup.body
            
            if content_div:
                # Remove scripts and styles
                for element in content_div(['script', 'style', 'nav', 'header', 'footer']):
                    element.decompose()
                text = content_div.get_text(separator='\n', strip=True)
                return text
            return ""
        except Exception as e:
            print(f"Error fetching document from Adilet")
            return None
