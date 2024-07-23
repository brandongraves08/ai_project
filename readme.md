# RAG Chatbot

## Overview

This project implements a standalone Question Answering (QA) chatbot using Retrieval-Augmented Generation (RAG). The chatbot uses a combination of local documents as its knowledge base to provide dynamic and contextually relevant responses.

## Features

- RAG-based response generation for dynamic answers
- Ability to process and use information from various file types (txt, pdf, json, csv, html, md)
- Uses HuggingFace models for language understanding and generation
- Easy-to-use command-line interface for testing and interaction

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/brandongraves08/ai_project.git
   cd ai_project
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Prepare your data:
   - Create a `data` directory in the project root if it doesn't exist
   - Place your document files (pdf, txt, json, csv, html, md) in the `data` directory

## Usage

1. Run the chatbot:
   ```
   python rag_chatbot.py
   ```

2. Once initialized, you can start asking questions. Type your questions and press Enter.

3. To exit the chatbot, type 'quit' and press Enter.

## Project Structure

- `rag_chatbot.py`: Main script implementing the RAG-based chatbot
- `data/`: Directory for storing document files (not included in the repository)
- `requirements.txt`: List of Python dependencies
- `README.md`: This file, containing project documentation

## Customization

- To customize the knowledge base, add or remove documents from the `data` directory
- To use a different language model, modify the `model_name` parameter in the `RAGChatbot` initialization

## How It Works

1. The chatbot loads and processes documents from the `data` directory
2. It uses a text splitter to break documents into smaller chunks
3. These chunks are embedded and stored in a vector database (Chroma)
4. When a question is asked, the most relevant chunks are retrieved
5. The language model generates a response based on the retrieved information

## Troubleshooting

- If you see a message about "Number of requested results is greater than number of elements in index", ensure that your `data` directory contains multiple documents with sufficient content.
- You may need to adjust the `chunk_size` in the `RecursiveCharacterTextSplitter` if you're working with very small documents.

## Limitations

- The quality of responses depends on the documents provided in the `data` directory
- The chatbot may occasionally generate incorrect or inconsistent responses
- It doesn't maintain conversation context between questions

## Future Improvements

- Implement caching to improve response time
- Add support for multi-turn conversations
- Implement user feedback mechanisms for continuous improvement
- Add support for online resources as part of the knowledge base
- **Integrate Jira wiki support:** Future versions will include the ability to connect to and retrieve information from Jira wikis, expanding the knowledge base to include up-to-date company documentation.
- **Enhance RAG capabilities:** We plan to improve the Retrieval-Augmented Generation system to provide more accurate and context-aware responses, possibly by incorporating more advanced language models and retrieval techniques.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to the [GitHub repository](https://github.com/brandongraves08/ai_project).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.