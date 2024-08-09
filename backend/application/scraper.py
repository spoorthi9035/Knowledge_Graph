from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {
            'title': soup.find('title').text if soup.find('title') else 'No Title',
            'paragraphs': [p.text for p in soup.find_all('p')]
        }
        return data
    except requests.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        return None

def google_search(query, api_key, cse_id, num=8):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, num=num).execute()
        return res.get('items', [])
    except Exception as e:
        logger.error(f"Google Search API error: {e}")
        return []

def join_data(results):
    data = []
    for result in results:
        parsed_data = scrape_data(result['link'])
        if parsed_data:
            data.append(parsed_data)
    return data
