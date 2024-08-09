import logging
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from py2neo import Graph, Node, Relationship
import spacy
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NLP model
nlp = spacy.load("en_core_web_sm")

# Neo4j connection
graph = Graph("bolt://3.239.102.59:7687", auth=("neo4j", "weights-grasses-editors"))


def scrape_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {
            'title': soup.find('title').text if soup.find('title') else 'No Title',
            'paragraphs': [p.text for p in soup.find_all('p')],
            'links': [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
        }
        return data
    except requests.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        return None

def google_search(query, api_key, cse_id, num=6):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, num=num).execute()
        print(res)
        return res.get('items', [])
    except Exception as e:
        logger.error(f"Google Search API error: {e}")
        return []

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def clean_text(text):
    # Remove extra spaces, special characters, etc.
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

def normalize_text(text):
    # Convert to consistent capitalization
    text = text.lower()
    return text

def clean_and_normalize_data(data):
    cleaned_data = []
    for item in data:
        cleaned_item = {
            'title': clean_text(item['title']),
            'paragraphs': [normalize_text(clean_text(p)) for p in item['paragraphs']],
            'links': item.get('links', [])
        }
        cleaned_data.append(cleaned_item)
    return cleaned_data

def add_fpga(graph, fpga_name, specs):
    fpga_node = Node("FPGA", name=fpga_name)
    graph.create(fpga_node)
    for spec_name, spec_value in specs.items():
        spec_node = Node("Specification", name=spec_name, value=spec_value)
        graph.create(spec_node)
        rel = Relationship(fpga_node, "HAS_SPECIFICATION", spec_node)
        graph.create(rel)
    return fpga_node

def join_data(results):
    data = []
    for result in results:
        parsed_data = scrape_data(result['link'])
        if parsed_data:
            data.append(parsed_data)
            # Level 2 scraping
            for link in parsed_data['links']:
                sub_data = scrape_data(link)
                if sub_data:
                    data.append(sub_data)
    return data

def process_data(data):
    cleaned_data = clean_and_normalize_data(data)
    for item in cleaned_data:
        for paragraph in item['paragraphs']:
            entities = extract_entities(paragraph)
            for entity in entities:
                if entity[1] == "ORG":
                    add_fpga(graph, item['title'], {"paragraph": paragraph})
def main():
    query = "Altera FPGA specifications"
    api_key = "AIzaSyC9hUYw2Mxz5EIKq6tpYB-vsMNyHWklVZM"
    cse_id = "61a3539b8227a4462"
    search_results = google_search(query, api_key, cse_id)
    print("\ndone with search result\n")
    scraped_data = join_data(search_results)
    print("\ndone with scraping\n")
    process_data(scraped_data)
    print("done")

if __name__ == "__main__":
    main()
