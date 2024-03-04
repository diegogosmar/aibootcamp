# Complete RAG module with OpenAI, Diego Gosmar, 2024
# It takes a user's query, generates an embedding for it, and then retrieves the most similar embeddings from the FAISS index. 
# This script will rely on the embeddings you've stored in embeddings.index

import openai
import faiss
import numpy as np
import json

# Define your QUERY PROMPT and ROLE here
#PROMPT = "What is the main theme of Alice in Wonderland?"
#PROMPT = "What's the unit price of the engine oil filter?"
PROMPT = "What's the order shipment address?"
#ROLE_CONTENT = "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."
ROLE_CONTENT = "You are an assitant providing order information."

OPENAI_API_KEY_PATH = '../OpenAI.key'  # Path to your OpenAI API key file
FAISS_INDEX_PATH = 'embeddings.index'
MODEL_FOR_EMBEDDING = "text-embedding-ada-002"
MODEL_FOR_COMPLETION = "gpt-4-0125-preview"

def get_openai_api_key(key_path):
    try:
        with open(key_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Failed to read OpenAI API key from {key_path}: {e}")
        return None

openai.api_key = get_openai_api_key(OPENAI_API_KEY_PATH)

def generate_query_embedding(query):
    response = openai.Embedding.create(input=query, model=MODEL_FOR_EMBEDDING)
    embedding = response['data'][0]['embedding']
    return np.array([embedding], dtype='float32')

def load_faiss_index(index_path):
    return faiss.read_index(index_path)

def retrieve_similar_embeddings(query_embedding, index, k=5):
    D, I = index.search(query_embedding, k)
    return I[0]

def get_text_segments_for_indices(indices):
    with open('embeddings_with_text.json', 'r') as file:
        data = json.load(file)
    # Ensure data is a list of dictionaries each containing a "text" key
    texts = []
    for index in indices:
        if index < len(data) and "text" in data[index]:
            texts.append(data[index]["text"])
        else:
            texts.append("Text not found for index: " + str(index))
    return texts

def generate_response_with_context(augmented_prompt, model=MODEL_FOR_COMPLETION):
    # Print the augmented prompt to the console
    print("Augmented Prompt:\n", augmented_prompt)

    response = openai.ChatCompletion.create(
      model=model,
      messages=[
       # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."}
        {"role": "system", "content": ROLE_CONTENT},
        {"role": "user", "content": augmented_prompt}
      ]
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    # User prompt/query: The initial question or statement from the user.
    query = PROMPT
    
    # Embedding of the user query: Converts the user's query into a vector using OpenAI's embedding model.
    query_embedding = generate_query_embedding(query)
    
    # Upload of the document.txt Vector DB indexes (embedding.index): Loads the pre-constructed FAISS index 
    # that contains embeddings of the document segments.
    index = load_faiss_index(FAISS_INDEX_PATH)
    
    # Similarity search between the Vector indexes (document.txt) and the embedded query: 
    # Finds the document segments (embeddings) most similar to the query embedding.
    similar_indices = retrieve_similar_embeddings(query_embedding, index, k=5)
    
    # Retrieval of the document.txt segment related to the similarity search: 
    # Maps the indices of the similar embeddings back to their corresponding text segments.
    context_segments = get_text_segments_for_indices(similar_indices)
    
    # Generation of the augmented new prompt/query for the LLM (OpenAI): 
    # Prepares a new prompt that combines the original query with the context segments for a more informed response.
    augmented_prompt = "\n".join(context_segments) + "\n\n" + query
    
    # LLM (OpenAI) response to the augmented prompt: Generates a response based on the augmented prompt using an OpenAI model.
    response = generate_response_with_context(augmented_prompt)
    
    print("Response:", response)

if __name__ == "__main__":
    main()
