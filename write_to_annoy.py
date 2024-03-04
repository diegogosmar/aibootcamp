# Vector DB management, Annoy, Diego Gosmar, 2024
# Import embeddings.json file and create the embeddings.ann vector DB

import json
from annoy import AnnoyIndex

# Load embeddings from file
with open('embeddings.json', 'r') as file:
    embeddings = json.load(file)

# Assume each embedding is of size 1536
f = 1536
t = AnnoyIndex(f, 'angular')

# Add embeddings to Annoy
for i, embedding in enumerate(embeddings):
    t.add_item(i, embedding)

# Build the Annoy index
t.build(10)  # The number 10 is a parameter that affects the build speed and index accuracy
t.save('embeddings.ann')

print("Annoy index created and saved.")

# Print the number of vectors in the DB
print("Number of vectors in the DB:", t.get_n_items())