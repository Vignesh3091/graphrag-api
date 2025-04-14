from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_core import vector_query_graph, generate_answer_from_context

app = FastAPI()

class Query(BaseModel):
    question: str
    limit: int = 5

@app.post("/rag-answer")
async def rag_answer(q: Query):
    results = vector_query_graph(q.question, limit=q.limit)
    answer = generate_answer_from_context(results, q.question)
    return {
        "question": q.question,
        "context_used": results,
        "answer": answer
    }

@app.post("/rag-retrieve")
async def rag_retrieve(q: Query):
    results = vector_query_graph(q.question, limit=q.limit)
    return {
        "question": q.question,
        "context_matches": results
    }
