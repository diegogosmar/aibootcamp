// RAG module with OpenAI, Diego Gosmar, 2024 //

const axios = require('axios');
const fs = require('fs').promises; // Import promises from fs for async file reading

async function getOpenAIKey() {
  try {
    const key = await fs.readFile('../OpenAI.key', 'utf8'); // Read the file content as a string
    return key.trim(); // Trim any newline or whitespace
  } catch (error) {
    console.error('Error reading OpenAI key:', error);
    return null;
  }
}

// Embedding Generation with OpenAI API model: "text-embedding-ada-002"
async function generateEmbedding(text) {
  try {
    const openAIKey = await getOpenAIKey(); // Retrieve the API key
    if (!openAIKey) {
      throw new Error('OpenAI key not found or is invalid');
    }

    const response = await axios.post(
      'https://api.openai.com/v1/embeddings',
      {
        model: "text-embedding-ada-002", // Choose the model
        input: text,
      },
      {
        headers: {
          'Authorization': `Bearer ${openAIKey}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data.data[0].embedding; // Return embedding vector
  } catch (error) {
    console.error('Error generating embedding:', error);
    return null;
  }
}

// Embedding Generation OpenAI API model function call
const text = `
Order Number: ACME-2024-005 Shipment Address:
Acme Ltd Warehouse
789 Storage Lane, Tech City
Billing Address:
Acme Ltd
123 Business Road, Tech City
`;
generateEmbedding(text).then(embedding => {
  console.log('Embedding:', embedding);
});
