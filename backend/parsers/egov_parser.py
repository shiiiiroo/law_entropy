import requests
import urllib.parse
import urllib3
from typing import List, Dict, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EGovParser:
    BASE_URL = "https://data.egov.kz/api/v4"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Search for datasets on Open Data portal data.egov.kz.
        """
        encoded_query = urllib.parse.quote_plus(query)
        # Endpoint for searching datasets
        search_url = f"{self.BASE_URL}/search/dataset?query={encoded_query}&from=0&size={limit}"
        
        try:
            response = self.session.get(search_url, timeout=15, verify=False)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if data and 'hits' in data and 'hits' in data['hits']:
                for hit in data['hits']['hits']:
                    source = hit.get('_source', {})
                    dataset_id = source.get('id')
                    title = source.get('titleKk') or source.get('titleRu')
                    # API returns metadata. We can construct a dataset URL or point to API
                    if title and dataset_id:
                        results.append({
                            "id": dataset_id,
                            "title": title,
                            "url": f"https://data.egov.kz/datasets/view?index={dataset_id}",
                            "source": "data.egov.kz"
                        })
            return results
        except Exception as e:
            print(f"Error searching eGov Open Data: {e}")
            # Fallback for demonstration if API blocks generic requests (403/WAF)
            v = query.lower()
            if 'налог' in v or 'труд' in v:
                return [{
                    "id": "mock_data_1", 
                    "title": f"Открытые данные по запросу '{query}' (Демо)", 
                    "url": "https://data.egov.kz", 
                    "source": "data.egov.kz (Mock)"
                }]
            return []

    def get_document_text(self, dataset_id: str, limit: int = 10) -> Optional[str]:
        """
        Fetch the content of a specific dataset from data.egov.kz Open Data API.
        Since datasets are structured data, we convert JSON to text representation.
        """
        url = f"{self.BASE_URL}/{dataset_id}/v1?from=0&size={limit}"
        
        try:
            if dataset_id == "mock_data_1":
                return "Демонстрационный текст датасета из Открытых Данных Казахстана.\nСтрока 1: Обсуждение нормативно-правового акта о налогах.\nСтрока 2: Внесение изменений в статьи кодекса."
            response = self.session.get(url, timeout=15, verify=False)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return ""
                
            text_lines = []
            text_lines.append(f"Dataset Data (ID: {dataset_id}):")
            
            # Usually data is a list of dictionaries representing rows
            if isinstance(data, list):
                for i, row in enumerate(data):
                    text_lines.append(f"Row {i+1}:")
                    for k, v in row.items():
                        text_lines.append(f" - {k}: {v}")
            elif isinstance(data, dict):
                for k, v in data.items():
                    text_lines.append(f" {k}: {v}")
                    
            return "\n".join(text_lines)
            
        except Exception as e:
            print(f"Error fetching dataset {dataset_id} from eGov: {e}")
            return None
