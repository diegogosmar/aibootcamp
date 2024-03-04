# RAG with OpenAI examples

## Basic Embedding example with node.js
See openai_basic.js for details<br>

## Basic Chunking example with node.js
See openai_chunks.js for details<br>

## Chunking example: it reads Document, embeds, chunks and stores the results in a json file (embedding.json)
See openai_chunks_file.js for details<br>

## Read embeddings.json file and write into the embeddings.ann Annoy vector DB
python write_to_annoy.py

## Read embeddings.json file and write into the embeddings.index FAISS vector DB
python write_to_faiss.py

## Indexing + metadata (chunk of text) inside embeddings_with_text.json
node openai_chunks_file_indexing.js
