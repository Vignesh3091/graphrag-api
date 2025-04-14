## GraphRAG API

An end-to-end GraphRAG system designed to work efficiently within free-tier constraints. It processes  XML content (e.g., Simplified to steps and instructions from a John Deere troubleshooting manual), stores structured data in Neo4j as a graph, retrieves relevant information (graph based) and semantic vector search, and generates contextual answers using a LLM, all exposed through a FastAPI backend deployed on Render.
---

## What I have done:

- Parses a complex **XML technical manual** (e.g. service instructions) - load_xml_into_neo4f._aura.py
- Extracts relevant tags with their textual content
- Pushes them into a **Neo4j Aura** graph database with relationships
- Performs **semantic similarity search** using Sentence Transformers (`all-MiniLM-L6-v2`) after quering with relationship  
- Optionally generates **LLM-based natural language answers** using HuggingFace's `flan-t5-large` #can use base model
- Provides a live, deployable **FastAPI server** to expose these as a public API

---

## Tech Stack
Graph DB          Neo4j Aura](https://neo4j.com/cloud/aura)  
Vector Embedding  `sentence-transformers` (`all-MiniLM-L6-v2`)  
Language Model    :HuggingFace `google/flan-t5-large`     #can use base model      
API Framework     :FastAPI  
Deployment        :https://render.com  
API               : https://graphrag-api-smwh.onrender.com/docs  


---

sample Screenshots from notebook for reference - jupyter notebook: graphRAG_Final_aura.ipynb

user_question = "How do I replace headlight assembly?"  
results = vector_query_graph(user_question, limit=3)  
generate_answer_from_context(results =results,user_question =  user_question)  

![how to change headlight](https://github.com/user-attachments/assets/5bc625b3-6f14-456f-b199-88fea437549d)


user_question = "How to prevent starter damage?"  
results = vector_query_graph(user_question, limit=3)  
generate_answer_from_context(results =results,user_question =  user_question)  
![how to prevent starter damage](https://github.com/user-attachments/assets/c60868f5-d905-4697-8e90-2ea26047d525)

