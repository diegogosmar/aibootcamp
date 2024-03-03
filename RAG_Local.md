# Local RAG example
![Image Alt text](/images/localrag.jpg

##Builiding blocks<br>
Ollama: to run an LLM locally and expose it to the web app.<br>
Transformers.js: to run open source Nomic embeddings in the browser and embed the user queries.<br>
Voy: as the vector store, fully WASM in the browser to vectorize the docs and perfom similarity searches.<br>
LangChain.js: to call the models, perform retrieval, and generally orchestrate all the pieces.<br>
<br>
git clone https://github.com/jacoblee93/fully-local-pdf-chatbot.git<br>
yarn <br>
npm run-script dev<br>
<br>
OLLAMA_ORIGINS=http://localhost:3000 OLLAMA_HOST=127.0.0.1:11435 ollama serve<br>
OLLAMA_HOST=127.0.0.1:11435 ollama pull mistral<br>
<br>
Access via: http://localhost:3000/<br>
