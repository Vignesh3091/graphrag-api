import os
from transformers import pipeline
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer, util

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DB = os.getenv("NEO4J_DB")

print("NEO4J_URI:", repr(os.getenv("NEO4J_URI")))


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
model = SentenceTransformer("all-MiniLM-L6-v2")

# def vector_query_graph(user_question, limit=5):
#     with driver.session(database=NEO4J_DB) as session:
#         result = session.run("MATCH (n) WHERE n.content IS NOT NULL RETURN n.id AS id, n.tag AS tag, n.content AS content")
#         candidates = [r.data() for r in result]
#     question_emb = model.encode(user_question, convert_to_tensor=True)
#     scored = [(util.pytorch_cos_sim(question_emb, model.encode(c["content"], convert_to_tensor=True)).item(), c) for c in candidates]
#     return [r[1] for r in sorted(scored, key=lambda x: x[0], reverse=True)[:limit]]

def vector_query_graph(user_question, limit=5):
    try:
        with driver.session(database=NEO4J_DB) as session:
            result = session.run(
                "MATCH (n) WHERE n.content IS NOT NULL RETURN n.id AS id, n.tag AS tag, n.content AS content"
            )
            candidates = [r.data() for r in result]
        question_emb = model.encode(user_question, convert_to_tensor=True)
        scored = [(util.pytorch_cos_sim(question_emb, model.encode(c["content"], convert_to_tensor=True)).item(), c) for c in candidates]
        return [r[1] for r in sorted(scored, key=lambda x: x[0], reverse=True)[:limit]]
    except Exception as e:
        print(" vector_query_graph ERROR:", e)
        return []


def build_prompt(context, question):
    return f"""
You are a helpful technical assistant.

Below are service manual excerpts:

{context}

Question: {question}
Answer using detailed, full sentences:
"""

llm_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    device_map= None,
    torch_dtype="auto"
)

# def generate_answer_from_context(results, user_question):
#     if not results:
#         return "No relevant info found."
#     context = "\n".join([f"{r['tag']} ({r['id']}): {r['content']}" for r in results if r.get("content")])
#     prompt = build_prompt(context, user_question)
#     output = llm_pipeline(prompt, max_new_tokens=512, temperature=0.7, top_k=50, top_p=0.9, repetition_penalty=1.2)
#     return output[0]["generated_text"].split("Answer:")[-1].strip()

def generate_answer_from_context(results, user_question):
    try:
        if not results:
            return "No relevant info found."
        context = "\n".join([f"{r['tag']} ({r['id']}): {r['content']}" for r in results if r.get("content")])
        prompt = build_prompt(context, user_question)
        output = llm_pipeline(prompt, max_new_tokens=512, temperature=0.7, top_k=50, top_p=0.9, repetition_penalty=1.2)
        return output[0]["generated_text"].split("Answer:")[-1].strip()
    except Exception as e:
        print("LLM ERROR:", e)
        return "LLM failed to generate a response."

