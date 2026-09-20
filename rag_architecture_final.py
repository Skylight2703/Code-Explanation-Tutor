from input import get_code_from_file, sample_program, query
import faiss
import numpy as np
code = get_code_from_file(sample_program)
chunks = [line.strip() for line in code.split("\n") if line.strip()]
'''for i,chunk in enumerate(chunks):
    print(f'{i} : {chunk}')
    print('-'*75)'''
#Creation of embeddings of file
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)
embedding = model.encode(chunks)
#print("Number of chunks: ", len(chunks))
#print("Shape of embedding: ",embedding.shape)
#Creation of FAISS index

dimension = embedding.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embedding).astype('float32'))
#print("Number of vectors in the index: ", index.ntotal)
##converting user query to embedding and searching in the index
query_embedding = model.encode([query])
k = 5  # Number of nearest neighbors to retrieve
D, I = index.search(np.array(query_embedding).astype('float32'),k)
#print("Distances: ", D)
#print("Indices: ", I)
'''for i in I[0]:
    print("Chunk: ", chunks[i])
    print('-'*75)'''
#printing the result
results = [chunks[i] for i in I[0]]
#print("Results: ", results)
