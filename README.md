# GraphRAG API

An end-to-end GraphRAG system that combines XML-parsed content ( Related like steps, content, etc, simplified for free tier ) for the xml shared on john deere troubshooting, Neo4j graph storage, semantic vector search, and LLM-based response generation — all exposed via FastAPI and deployed on Render.

---

## What I have done:

- Parses a complex **XML technical manual** (e.g. service instructions)
- Extracts relevant tags with their textual content
- Pushes them into a **Neo4j Aura** graph database with relationships
- Performs **semantic similarity search** using Sentence Transformers (`all-MiniLM-L6-v2`)
- Optionally generates **LLM-based natural language answers** using HuggingFace's `flan-t5-large` #can use base model
- Provides a live, deployable **FastAPI server** to expose these as a public API

---

## Tech Stack
Graph DB          Neo4j Aura](https://neo4j.com/cloud/aura) 
Vector Embedding  `sentence-transformers` (`all-MiniLM-L6-v2`) 
Language Model    :HuggingFace `google/flan-t5-large`     #can use base model     
API Framework     :FastAPI              
Deployment        :https://render.com   


---

