

import xml.etree.ElementTree as ET
import asyncio
from neo4j import AsyncGraphDatabase
from sentence_transformers import SentenceTransformer, util
import xml.etree.ElementTree as ET
from neo4j import GraphDatabase


# === CONFIG ===
NEO4J_URI = "neo4j+s://ddf3e3b8.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "c5bFc-_D_rviELGy0J7I_LC2Ltbhgr1eJ-_fOODWOiA"
NEO4J_DB = "neo4j"
XML_FILE = r"D:\GraphRAG_Project\omdxe11337.xml"
RELEVANT_TAGS = {"component", "procedure", "step"}
BATCH_SIZE = 200

# === GLOBAL ===
nodes = []
relationships = []
model = SentenceTransformer('all-MiniLM-L6-v2')


# === CONNECT ===
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# === Helpers ===
def clean_tag(tag):
    return tag.split("}")[-1]

def extract_text(elem):
    texts = [elem.text.strip()] if elem.text and elem.text.strip() else []
    for child in elem:
        texts.append(extract_text(child))
        if child.tail and child.tail.strip():
            texts.append(child.tail.strip())
    return " ".join(texts).strip()

def process_element(elem, parent=None):
    tag = clean_tag(elem.tag)
    if tag in RELEVANT_TAGS:
        node_id = elem.attrib.get("id", f"{tag}_{hash(elem)}")
        content = extract_text(elem)
        props = {"id": node_id, "tag": tag, "content": content, **elem.attrib}
        nodes.append({"id": node_id, "tag": tag, "props": props})
        if parent:
            relationships.append({
                "from_id": parent["id"],
                "to_id": node_id,
                "from_label": parent["tag"],
                "to_label": tag,
                "type": "CONTAINS"
            })
        parent = {"id": node_id, "tag": tag}
    for child in elem:
        process_element(child, parent)

async def write_batch(tx, node_batch, rel_batch):
    for node in node_batch:
        await tx.run("""
            MERGE (n:{tag} {id: $id})
            SET n += $props
        """.replace("{tag}", node['tag']), id=node["id"], props=node["props"])

    for rel in rel_batch:
        await tx.run(f"""
            MATCH (a:{rel['from_label']} {{id: $from_id}}), (b:{rel['to_label']} {{id: $to_id}})
            MERGE (a)-[:{rel['type']}]->(b)
        """, from_id=rel["from_id"], to_id=rel["to_id"])

async def load_to_neo4j():
    driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    async with driver.session(database=NEO4J_DB) as session:
        for i in range(0, len(nodes), BATCH_SIZE):
            node_batch = nodes[i:i + BATCH_SIZE]
            rel_batch = relationships[i:i + BATCH_SIZE]
            await session.execute_write(write_batch, node_batch, rel_batch)
    await driver.close()

async def clear_database():
    driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    async with driver.session(database=NEO4J_DB) as session:
        await session.run("MATCH (n) DETACH DELETE n")
    await driver.close()

    
async def main():
    await clear_database()
    print(" Parsing XML...")
    tree = ET.parse(XML_FILE)
    process_element(tree.getroot())
    print(f"Parsed {len(nodes)} nodes and {len(relationships)} relationships.")
    print("Loading to Neo4j...")
    await load_to_neo4j()
    print("Done!")
