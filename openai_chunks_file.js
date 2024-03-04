// RAG module with OpenAI, Diego Gosmar, 2024 //
// Read external data from DOCUMENT //
// Store the embedding on the file embeddings.json //

const fs = require('fs').promises;
const axios = require('axios');

// Define the DOCUMENT constant with the file path
//const DOCUMENT = 'document.txt';
const DOCUMENT = 'order.txt';

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

  const chunks = chunkText(documentText, chunkLength);
  const embeddings = []; // Array to hold embeddings

  for (const chunk of chunks) {
    const embedding = await generateEmbedding(chunk, openAIKey);
    if (embedding) {
      embeddings.push(embedding); // Add the generated embedding to the array
    }
  }

  // After processing all chunks, save the embeddings array to a file
  await saveEmbeddingsToFile(embeddings, 'embeddings.json');
  console.log('Finished processing document and saved embeddings.');
}

// Define saveEmbeddingsToFile
async function saveEmbeddingsToFile(embeddings, filename) {
    try {
        await fs.writeFile(filename, JSON.stringify(embeddings), 'utf8');
        console.log('Saved embeddings to file');
    } catch (err) {
        console.error('Error writing to file', err);
    }
}

// Read external document
async function readDocumentText(filePath) {
  try {
    return await fs.readFile(filePath, 'utf8');
  } catch (error) {
    console.error('Error reading document file:', error);
    return '';
  }
}

async function main() {
  const filePath = DOCUMENT; // Adjust the file path as necessary
  const documentText = await readDocumentText(filePath);
  const chunkLength = 120; // Define the maximum length of each chunk

  if (documentText) {
    await processDocumentInChunks(documentText, chunkLength);
    console.log('Document processing complete.');
  } else {
    console.log('Document text is empty or file could not be read.');
  }
}

main();
