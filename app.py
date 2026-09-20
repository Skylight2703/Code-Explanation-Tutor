import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Prevent input() from hanging the backend during imports
if not sys.stdin.isatty():
    sys.stdin = open(os.devnull, 'r')

# Import your existing backend logic
try:
    from input import get_code_from_file, sample_program
    from rag_architecture_final import results
    import ollama
except Exception as e:
    print(f"Error loading dependencies: {e}")

app = FastAPI(title="Code Explanation Tutor API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryPayload(BaseModel):
    query: str

@app.get("/")
def serve_index():
    if os.path.exists("frontend.html"):
        return FileResponse("frontend.html")
    return {"status": "Backend running", "message": "frontend.html not found"}

@app.get("/api/code")
def get_code():
    """Returns source file contents."""
    try:
        code_text = get_code_from_file(sample_program)
        return {"code": code_text, "file_path": sample_program}
    except Exception as e:
        return {"code": f"Error: {str(e)}", "file_path": sample_program}

@app.get("/api/chunks")
def get_chunks():
    """Returns top RAG chunks retrieved from FAISS."""
    return {"chunks": results}

@app.post("/ask")
def query_tutor(payload: QueryPayload):
    """Processes questions and streams LLM output with anti-hallucination guardrails."""
    user_query = payload.query.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        code = get_code_from_file(sample_program)
        context = "\n\n---\n\n".join(results)

        prompt = f"""You are a professional Code Explaining Tutor. Answer the query with respect to the code provided only.
If the answer cannot be found in the code, reply: "I cannot fetch the answer or Irrelevant query".

---Code Context---
{context}

---Full Code---
{code}

---User Question---
{user_query}
"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )

        return {
            "query": user_query,
            "answer": response["message"]["content"],
            "retrieved_chunks": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama execution error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)