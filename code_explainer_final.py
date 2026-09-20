import ollama
from input import get_code_from_file, sample_program, query 
from rag_architecture_final import results
code = get_code_from_file(sample_program)


final = "\n\n---\n\n ".join(results)
prompt = f'''You are a professional Code Explainging Tutor and you will answer the query with respect 
to the code provided only. If the answer cannot be found in the code then answer "I cannot fetch the
answer or Irrelevant query or the query is completely irrelevant dismiss the query and return an error type message". 

---Code---
{code}
---Query---
{query}
---Answer---
'''

# 3. RAG Context Integration Function
response = ollama.chat(
    model= "llama3",
    messages=[
        {"role": "user", "content": f"{query}\n\nHere is the code:\n{code}"},
    ],
    stream=True
)
for chunk in response:
    print(chunk['message']['content'], end='', flush=True)

