# Cheshire Cat hands-on
![Image Alt text](/images/cat.jpg)

##setup and Launch (local)

1.Install and launch Docker on your machine<br>

2.1 Launching the cat (fast way):<br>
docker run --rm -it -p 1865:80 ghcr.io/cheshire-cat-ai/core:latest<br>
<br>
2.2 Launching the cat (preferable way):<br>
cd your_new_cat_folder<br>
<br>
Create docker-compose.yml<br>
<br>
_version: '3.7'<br>
<br>
services:<br>
<br>
  cheshire-cat-core:<br>
    image: ghcr.io/cheshire-cat-ai/core:latest<br>
    container_name: cheshire_cat_core<br>
    ports:<br>
      - ${CORE_PORT:-1865}:80<br>
    environment:<br>
      - PYTHONUNBUFFERED=1<br>
      - WATCHFILES_FORCE_POLLING=true<br>
    volumes:<br>
      - ./static:/app/cat/static<br>
      - ./plugins:/app/cat/plugins<br>
      - ./data:/app/cat/data_<br>
<br>
Launch the cat:<br>
docker compose up –d<br>
<br>
To check the logs:<br>
docker compose logs -f<br>
<br>
You should see:<br>
cheshire_cat_core  | Cat REST API:   http://localhost:1865/docs<br>
cheshire_cat_core  | Cat PUBLIC:     http://localhost:1865/public<br>
cheshire_cat_core  | Cat ADMIN:      http://localhost:1865/admin<br>
<br>
Open the GUI:<br>
http://localhost:1865/admin/<br>
<br>
Step 1: set you LLM in the Settings<br>
Step 2: Try a user query:<br>
Who was Giulio Cesare?<br>
Step 3: try a RAG with specific user query, i.e.:<br>
What’s the shipment address inside the order ACME-2024-005?<br>
Upload the ACME-2024-005 pdf order and retry the user query<br>
Memory: WIPE to reset the memory to remove the document from the Declarative mem<br>
<br>
Step 3: create your plugin and install it<br>
cd core/cat/plugins/<br>
create the new plugin folder, i.e. poetic_book_seller<br>
You need two files in your new plugin folder:<br>
<br>
├── core<br>
│   ├── cat<br>
│   │   ├── plugins<br>
|   |   |   ├── poetic_book_seller<br>
|   |   |   |   ├ poetic_book_seller.py<br>
|   |   |   |   ├ plugin.json<br>
<br>
The plugin.json file contains plugin's title and description, and is useful in the Admin Portal to recognize the plugin and activate/deactivate it.<br>
<br>
plugin.json example:<br>

{<br>
    "name": "Poetic Book Seller",<br>
    "description": "Description of poetic_book_seller"<br>
}<br>
<br>
The poetic_sock_seller.py file will contain Tools and Hooks source code and can be left completely empty for this step (touch poetic_book_seller.py).<br>
<br>
Open the GUI:<br>
http://localhost:1865/admin/<br>
Go to the Plugin tab of the Admin Portal. Your empty plugin will be there, activate it.<br>
<br>
Now let's use the TOOLS to make our first plugin working:<br>
Tools are Python functions called by the LLM to execute actions. They are made of two parts: the first one contains instructions that explain the LLM when and how to call function; the second one contains the actual code to execute.<br>
<br>
_cat poetic_book_seller.py <br>
from cat.mad_hatter.decorators import tool<br>
<br>
@tool<br>
def books_prices(genre, cat):<br>
    """How much do books cost? Input is the book genre please."""<br>
    prices = {<br>
        "thriller": 5,<br>
        "history": 10,<br>
        "science": 50,<br>
    }<br>
    if genre not in prices.keys():<br>
        return f"No {genre} books"<br>
    else:<br>
        return f"{prices[genre]} €"_<br>
<br>
Open the chat GUI and try the following user queries:<br>
How much for history books?<br>
How much for thriller books?<br>
How much for science books?<br>
<br>
