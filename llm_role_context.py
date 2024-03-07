# Langsmith hands on, Diego Gosmar, 2024

# Import necessary libraries
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import LangChain after environment variables are loaded
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

def main():
    # Initialize the ChatOpenAI model with environment variables
    llm = ChatOpenAI()

    # Define the role and context
    role = "You are an assistant providing order information."
    context = """
    Order Number: ACME-2024-005
    Shipment Address: Acme Ltd Warehouse, 789 Storage Lane, Tech City
    Billing Address: Acme Ltd, 123 Business Road, Tech City
    """

    # Combine the role, context, and the user's question into a single prompt
    prompt = f"{role}\n{context}\nWhat is the shipping address in order ACME-2024-005?"

    # Make a prediction
    response = llm.invoke(prompt)

    # Print the response
    print("\n\n" + "====================")
    print(response)
    print("====================" + "\n\n")

if __name__ == "__main__":
    main()

