from flask import Blueprint, request, jsonify, current_app
from .scraper import google_search, join_data
from .knowledge_graph import create_knowledge_graph, query_knowledge_graph
from .db import get_graph
from .nlp import extract_information, map_to_cypher

main = Blueprint('main', __name__)

@main.route('/search_and_scrape', methods=['POST'])
def search_and_scrape():
    topic = request.json.get('topic')
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    api_key = current_app.config['GOOGLE_API_KEY']
    cse_id = current_app.config['CSE_ID']
    results = google_search(topic, api_key, cse_id)
    scraped_data = join_data(results)
    
    for data in scraped_data:
        create_knowledge_graph(data)
    
    return jsonify({"message": "Data scraped and knowledge graph created successfully", "data": scraped_data})

@main.route('/query_fpga', methods=['POST'])
def query_fpga():
    topic = request.json.get('topic')
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    graph = get_graph()
    query = f"""
    MATCH (f:FPGA)
    WHERE f.name CONTAINS '{topic}'
    RETURN f.on_chip_ram as on_chip_ram
    """
    result = graph.run(query).data()
    return jsonify(result)

@main.route('/natural_query', methods=['POST'])
def natural_query():
    user_query = request.json.get('message')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Debugging: Print the user query
    print(f"User Query: {user_query}")

    info_type, entity = extract_information(user_query)
    
    # Debugging: Print the extracted information
    print(f"Extracted Info Type: {info_type}, Entity: {entity}")

    if not info_type or not entity:
        return jsonify({"error": "Unable to extract information from query"}), 400

    cypher_query = map_to_cypher(info_type, entity)
    
    # Debugging: Print the generated Cypher query
    print(f"Generated Cypher Query: {cypher_query}")

    graph = get_graph()
    result = graph.run(cypher_query).data()
    
    # Debugging: Print the result of the Cypher query
    print(f"Query Result: {result}")

    if not result:
        return jsonify({"error": "No data found for the query"}), 404

    return jsonify(result)


@main.route('/test', methods=['GET'])
def test():
    return "Working"