from py2neo import Node, Relationship
from .db import get_graph

def create_knowledge_graph(data):
    graph = get_graph()
    tx = graph.begin()
    title_node = Node("Topic", name=data['title'])
    tx.create(title_node)
    for paragraph in data['paragraphs']:
        para_node = Node("Paragraph", content=paragraph)
        tx.create(para_node)
        tx.create(Relationship(title_node, "CONTAINS", para_node))
    tx.commit()

def query_knowledge_graph(query):
    graph = get_graph()
    result = graph.run(query).data()
    return result
