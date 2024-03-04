# Vector DB management, Annoy, Diego Gosmar, 2024
# Import embeddings.json file and create the embeddings.array vector DB

import json
import numpy as np
import faiss

# Load embeddings from file
with open('embeddings.json', 'r') as file:
    embeddings = json.load(file)

# Convert embeddings list to a numpy array
embeddings_array = np.array(embeddings).astype('float32')

# Dimension of the vectors
d = embeddings_array.shape[1]

# Create a FAISS index
index = faiss.IndexFlatL2(d)  # L2 distance for similarity

# Add embeddings to the index
index.add(embeddings_array)

# Save the index
faiss.write_index(index, "embeddings.index")

print("FAISS index created and saved.")
