# Configuration settings for the Flask application
# Graph("bolt://3.235.124.82:7474", auth=("neo4j", "greenwich-executives-fireplug"))
# 7474 -> 7687
class Config:
    NEO4J_URI = "bolt://3.235.124.82:7687"
    #NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "documentations-marbles-satellites"
    GOOGLE_API_KEY = 'AIzaSyDg5iZ6VSGlFoN3DXdE5SaLy5Rn1wPPgGY'
    CSE_ID = '23d32205a4635492e'