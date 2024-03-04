// RAG module with OpenAI, Diego Gosmar, 2024 //
// Split the text into chunks of max lenght chunkLength and embed each chunk in one vector each one //

const fs = require('fs').promises;
const axios = require('axios');

async function getOpenAIKey() {
  try {
    const key = await fs.readFile('../OpenAI.key', 'utf8');
    return key.trim();
  } catch (error) {
    console.error('Error reading OpenAI key:', error);
    return null;
  }
}

async function generateEmbedding(text, openAIKey) {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/embeddings',
      {
        model: "text-embedding-ada-002",
        input: text,
      },
      {
        headers: {
          'Authorization': `Bearer ${openAIKey}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data.data[0].embedding;
  } catch (error) {
    console.error('Error generating embedding:', error);
    return null;
  }
}

function chunkText(text, maxLength) {
  let chunks = [];
  while (text.length > 0) {
    let chunkSize = maxLength;
    // Ensure not to cut in the middle of a word
    if (text.length > maxLength && text.charAt(maxLength) !== ' ' && text.charAt(maxLength - 1) !== ' ') {
      let lastSpace = text.lastIndexOf(' ', maxLength);
      chunkSize = lastSpace !== -1 ? lastSpace : maxLength;
    }
    chunks.push(text.substring(0, chunkSize).trim());
    text = text.substring(chunkSize).trim();
  }
  return chunks;
}

async function processDocumentInChunks(documentText, chunkLength) {
  const openAIKey = await getOpenAIKey();
  if (!openAIKey) {
    console.error('OpenAI key not found or is invalid');
    return;
  }

  // Split the document into chunks of the specified length
  const chunks = chunkText(documentText, chunkLength);

  for (const chunk of chunks) {
    const embedding = await generateEmbedding(chunk, openAIKey);
    console.log('Embedding for chunk:', chunk, '\n', embedding);
    // Handle the embeddings as needed
  }
}

// Example usage with a long document text and a specific chunk length
const documentText = "Your long document text goes here. This text will be split into manageable chunks based on the specified character length, ensuring that processing can occur without exceeding model input limits.";
const chunkLength = 120; // Define the maximum length of each chunk

processDocumentInChunks(documentText, chunkLength).then(() => {
  console.log('Finished processing document.');
});
