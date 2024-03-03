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
<br>
http://localhost:1865/admin/<br>
<br>
You should see:<br>
cheshire_cat_core  | Cat REST API:   http://localhost:1865/docs<br>
cheshire_cat_core  | Cat PUBLIC:     http://localhost:1865/public<br>
cheshire_cat_core  | Cat ADMIN:      http://localhost:1865/admin<br>
<br>

Step 1: open http://localhost:1865/admin and set you LLM in the Settings<br>
Try a user query:<br>
Who was Giulio Cesare?<br>
What’s the shipment address inside the order ACME-2024-005?<br>
Order upload pdf<br>
Memory: WIPE to reset the memory<br>
