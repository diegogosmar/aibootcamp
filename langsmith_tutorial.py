import os
from dotenv import load_dotenv
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset

# Load environment variables from .env file
load_dotenv()

# Import LangChain after environment variables are loaded
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

    # Create a Client
    client = Client()

    # Define the dataset name and description
    dataset_name = "Rap Battle Dataset"
    description = "A collection of rap battle prompts."

    # Initialize dataset variable
    dataset = None

    # Fetch all existing datasets
    existing_datasets = client.list_datasets()

    # Check if the dataset with the desired name already exists
    for existing_dataset in existing_datasets:
        if existing_dataset.name == dataset_name:
            dataset = existing_dataset
            print(f"Dataset '{dataset_name}' already exists.")
            break

    # If dataset does not exist, create a new one
    if dataset is None:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=description,
        )
        print(f"Dataset '{dataset_name}' created.")

    # Add examples to the dataset
    example_inputs = [
        "a rap battle between Atticus Finch and Cicero",
        "a rap battle between Barbie and Oppenheimer",
        "a Pythonic rap battle between two swallows: one European and one African",
        "a rap battle between Aubrey Plaza and Stephen Colbert",
    ]

    for input_prompt in example_inputs:
        client.create_example(
            inputs={"question": input_prompt},
            outputs=None,
            dataset_id=dataset.id,
        )

    # --------------------------------------------------------------
    # Evaluate Datasets with LLM
    # --------------------------------------------------------------

    eval_config = RunEvalConfig(
        evaluators=[
            "criteria",
            RunEvalConfig.Criteria("harmfulness"),
            RunEvalConfig.Criteria("misogyny"),
            RunEvalConfig.Criteria({
                "cliche": "Are the lyrics cliche? Respond Y if they are, N if they're entirely unique."
            }),
        ]
    )

    # Run evaluation on the dataset
    run_on_dataset(
        client=client,
        dataset_name=dataset_name,
        llm_or_chain_factory=llm,
        evaluation=eval_config,
    )

    # --------------------------------------------------------------
    # Different Ways of Creating Datasets in LangSmith
    # 1. Create a Dataset From a List of Examples (Key-Value Pairs)
    # --------------------------------------------------------------

    example_inputs = [
        ("What is the largest mammal?", "The blue whale"),
        ("What do mammals and birds have in common?", "They are both warm-blooded"),
        ("What are reptiles known for?", "Having scales"),
        (
            "What's the main characteristic of amphibians?",
            "They live both in water and on land",
        ),
    ]

    dataset_name = "Elementary Animal Questions"

    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Questions and answers about animal phylogenetics.",
    )

    for input_prompt, output_answer in example_inputs:
        client.create_example(
            inputs={"question": input_prompt},
            outputs={"answer": output_answer},
            dataset_id=dataset.id,
        )

    # --------------------------------------------------------------
    # Correctness: LangSmith Question-Answer Evaluation
    # 1. Evaluate Datasets That Contain Labels
    # --------------------------------------------------------------

    evaluation_config = RunEvalConfig(
        evaluators=[
            "qa",  # correctness: right or wrong
            "context_qa",  # refer to example outputs
            "cot_qa",  # context_qa + reasoning
        ]
    )

    run_on_dataset(
        client=client,
        dataset_name="Elementary Animal Questions",
        llm_or_chain_factory=llm,
        evaluation=evaluation_config,
    )

    # --------------------------------------------------------------
    # 2. Evaluate Datasets With Customized Criterias
    # --------------------------------------------------------------

    evaluation_config = RunEvalConfig(
        evaluators=[
            # You can define an arbitrary criterion as a key: value pair in the criteria dict
            RunEvalConfig.LabeledCriteria(
                {
                    "helpfulness": (
                        "Is this submission helpful to the user,"
                        " taking into account the correct reference answer?"
                    )
                }
            ),
        ]
    )

    run_on_dataset(
        client=client,
        dataset_name="Elementary Animal Questions",
        llm_or_chain_factory=llm,
        evaluation=evaluation_config,
    )

    # Print the response
    print("\n\n" + "====================")
    print(response)
    print("====================" + "\n\n")

if __name__ == "__main__":
    main()
