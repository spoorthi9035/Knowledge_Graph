# Knowledge_Graph
 
Project where I developed an Automated Knowledge Graph (KG) System that gathers information from the web, organizes it into a structured format, and allows users to interact with it through a simple chat interface.

 Key Highlights:
1. Web Data Collection:
 - The system automatically searches the web for information on specific topics (e.g, Tesla, Electric Vehicles, etc) using Google’s Search API.
 - It collects data from web pages using tools like BeautifulSoup, which extracts important information while filtering out unnecessary content.

2. Building the Knowledge Graph:
 - Using advanced natural language processing (NLP) techniques from SpaCy, the system identifies key pieces of information (like companies, products ) and how they are related.
 - This data is then stored in Neo4j, a specialized database that organizes information in a visual graph format, making it easy to see connections between different entities.

3. Interactive Chat Interface:
 - I built a user-friendly chat interface using ReactJS where people can ask questions like "What is the driving range of Tesla Model?" and get immediate, accurate answers from the knowledge graph.
 - The system also has the ability to create a document based on the collected data, making it easy to share or review the information.

Tools Used:
- Frontend: ReactJS for building the user interface.
- Backend: Flask to handle user requests and manage communication with the knowledge graph.
- Data Extraction: BeautifulSoup for web scraping and SpaCy for identifying key entities and relationships.
- Database: Neo4j to store and visualize the knowledge graph.

