from py2neo import Graph
from flask import current_app

def get_graph():
    if 'graph' not in current_app.config:
        current_app.config['graph'] = Graph(current_app.config['NEO4J_URI'], auth=(current_app.config['NEO4J_USER'], current_app.config['NEO4J_PASSWORD']))
    return current_app.config['graph']
