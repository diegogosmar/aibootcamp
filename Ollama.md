# ollama stuff

ollama installation:<br>
https://ollama.com/<br>

<br>
##Model downloads<br>
ollama pull llama2<br>
ollama pull mistral<br>
<br>
##Model run
ollama run llama2<br>
ollama run mistral<br>
<br>
##Model list
ollama list (get the list of pulled models)<br>
<br>
##Manage custom role for AI agent
nano Modelfile<br><br>
FROM llama2<br>
<br>
# set the temperature to 1 [higher is more creative, lower is more coherent]<br>
PARAMETER temperature 1<br>
<br>
# set the system message<br>
SYSTEM """<br>
Your name is Smart Library Agent. You are an AI assistant providing only information about Books and Authors. <br>
If the users ask anything else, gently explain them you can provide information only related to books.<br>
"""<br>
<br>
ollama create smartlibrary -f ./Modelfile <br>
ollama run smartlibrary<br>
i.e. Where can I order a good pizza in…?<br>
i.e. Who wrote the man and the sea?<br>
<br>
##Play with the API
curl http://localhost:11434/api/generate -d '{<br>
  "model": "smartlibrary",<br>
  "prompt": "Why is the sky blue?"<br>
}’<br>
<br>
curl http://localhost:11434/api/generate -d '{<br>
  "model": "smartlibrary",<br>
  "prompt": "What’s the latest book by Dan Brown?"<br>
}’<br>
<br>
NO STREAM:curl http://localhost:11434/api/generate -d "{<br>
  \"model\": \"smartlibrary\",<br>
  \"prompt\": \"What is the latest book by Dan Brown?\",<br>
  \"stream\": false<br>
}"<br>
<br>
