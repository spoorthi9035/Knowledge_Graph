import spacy

nlp = spacy.load('en_core_web_sm')

def extract_information(query):
    doc = nlp(query)
    info_type = None
    entity = None

    # Identify named entities and noun chunks
    for ent in doc.ents:
        if ent.label_ in ('ORG', 'PRODUCT', 'GPE'):
            entity = ent.text
            break  # We assume the first entity found is the main one

    if not entity:
        for chunk in doc.noun_chunks:
            if chunk.root.dep_ in ('nsubj', 'dobj'):
                entity = chunk.text
                break

    # Identify the main verb or noun as info_type
    for token in doc:
        if token.dep_ == 'ROOT' and token.pos_ in ('VERB', 'AUX', 'NOUN'):
            info_type = token.lemma_
            break

    return info_type, entity

def map_to_cypher(info_type, entity):
    info_mapping = {
        'ram': 'on_chip_ram',
        'manufacturer': 'manufacturer',
        'model': 'model',
        'fpga': 'name',  # Assuming a query asking about FPGA name
        'detail': 'detail'  # Fallback for details not explicitly mapped
    }

    # cypher_property = info_mapping.get(info_type, 'detail')
    cypher_property = info_type
    if cypher_property == 'detail':
        cypher_query = f"""
        MATCH (f:FPGA)
        WHERE f.name CONTAINS '{entity}'
        RETURN f
        """
    else:
        # cypher_query = f"""
        # MATCH (f)
        # WHERE f.name CONTAINS '{entity}'
        # RETURN f.{cypher_property} as {cypher_property}
        # """

        # cypher_query = f"""
        # MATCH (f)
        # WHERE f.name CONTAINS '{entity}'
        # RETURN f
        # """

        cypher_query = f"""
        MATCH (f)
        WHERE f.name CONTAINS '{entity}'
        OPTIONAL MATCH (f)-[r]-(connected)
        RETURN f, r, connected
        """
    return cypher_query
