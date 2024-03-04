// RAG module with OpenAI, Diego Gosmar, 2024 //
// Read external data from DOCUMENT //
// Store the embedding on the file embeddings_with_text.json //

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
    const embeddings = []; // To hold embeddings
    const texts = []; // To hold corresponding text segments

    for (const chunk of chunks) {
        const embedding = await generateEmbedding(chunk, openAIKey);
        if (embedding) {
            embeddings.push(embedding); // Add the generated embedding to the array
            texts.push(chunk); // Add the corresponding text to the texts array
        }
    }

    // Save embeddings and their corresponding text segments to a file
    await saveEmbeddingsToFile(embeddings, texts, 'embeddings_with_text.json');
    console.log('Finished processing document and saved embeddings and texts.');
}

async function saveEmbeddingsToFile(embeddings, texts, filename) {
    const data = embeddings.map((embedding, index) => ({
        embedding: embedding,
        text: texts[index] // Make sure each embedding is paired with its text
    }));
    try {
        await fs.writeFile(filename, JSON.stringify(data), 'utf8');
        console.log('Saved embeddings and texts to file.');
    } catch (err) {
        console.error('Error writing to file', err);
    }
}

// Read external document
async function readDocumentText(filePath) {
    try {
        const documentText = await fs.readFile(filePath, 'utf8');
        return documentText;
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
