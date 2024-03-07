# Basic Langsmith by Langchain examples

## Set your .env file
Create your Langchain for Langsmith account:<br>
https://www.langchain.com/<br>
<br>
Set your project in Langsmith (i.e. myproject)<br>
<br>
Create your own .env file<br>
LANGCHAIN_TRACING_V2="true"<br>
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"<br>
LANGCHAIN_API_KEY="your_langchain_key"<br>
LANGCHAIN_PROJECT="myproject"<br>
OPENAI_API_KEY="your_openAI_key"<br>
<br>
## Example of Python script with OpenAI + Langsmith monitoring
See llm_role_context.py for details<br>
