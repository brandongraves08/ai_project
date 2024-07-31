import json
from typing import List
import os
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, pipeline

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
)

class RAGChatbot:
    def __init__(self, data_directory: str, model_name: str = "google/flan-t5-large"):
        self.model_name = model_name
        self.embeddings = HuggingFaceEmbeddings()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = self._load_model(model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vectorstore = None
        self.qa_chain = None

        self.documents = self.load_documents(data_directory)
        self._setup()

    def _load_model(self, model_name):
        if "t5" in model_name.lower():
            return AutoModelForSeq2SeqLM.from_pretrained(model_name)
        else:
            return AutoModelForCausalLM.from_pretrained(model_name)

    def load_documents(self, directory: str) -> List[Document]:
        documents = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filename.endswith('.txt'):
                loader = TextLoader(filepath)
            elif filename.endswith('.pdf'):
                loader = PyPDFLoader(filepath)
            elif filename.endswith('.csv'):
                loader = CSVLoader(filepath)
            elif filename.endswith('.html'):
                loader = UnstructuredHTMLLoader(filepath)
            elif filename.endswith('.md'):
                loader = UnstructuredMarkdownLoader(filepath)
            elif filename.endswith('.json'):
                documents.extend(self.load_json(filepath))
                continue
            else:
                print(f"Unsupported file format: {filename}")
                continue
            documents.extend(loader.load())
        return documents

    def load_json(self, filepath: str) -> List[Document]:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return [Document(page_content=json.dumps(item)) for item in data]

    def _setup(self):
        texts = [doc.page_content for doc in self.documents]
        split_texts = self.text_splitter.split_text("\n\n".join(texts))
        
        print(f"Number of split texts: {len(split_texts)}")
        if not split_texts:
            raise ValueError("No texts to process. Make sure your data directory contains valid documents.")

        try:
            print("Attempting to create embeddings...")
            embeddings = self.embeddings.embed_documents(split_texts[:5])  # Test with a small subset
            print(f"Successfully created {len(embeddings)} embeddings.")
        except Exception as e:
            print(f"Error creating embeddings: {str(e)}")
            raise

        try:
            print("Attempting to create Chroma vectorstore...")
            self.vectorstore = Chroma.from_texts(split_texts, self.embeddings, persist_directory="./chroma_db")
            print("Successfully created Chroma vectorstore.")
        except Exception as e:
            print(f"Error creating Chroma vectorstore: {str(e)}")
            raise

        print("Setting up pipeline and QA chain...")
        if "t5" in self.model_name.lower():
            model_pipeline = pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer, max_length=1024, truncation=True)
        else:
            model_pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, max_length=1024, truncation=True)
        
        llm = HuggingFacePipeline(pipeline=model_pipeline)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        print("Setup complete.")

    def get_response(self, query: str) -> str:
        try:
            # Retrieve relevant documents
            docs = self.vectorstore.similarity_search(query, k=2)
            
            # Prepare context
            context = " ".join([doc.page_content for doc in docs])
            
            # Truncate context if it's too long
            max_context_length = 512  # Adjust as needed
            if len(context) > max_context_length:
                context = context[:max_context_length]
            
            # Prepare input for the model
            if "t5" in self.model_name.lower():
                input_text = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
            else:
                input_text = f"Given the following context:\n\n{context}\n\nAnswer the question: {query}\n\nAnswer:"

            # Tokenize and truncate if necessary
            tokens = self.tokenizer.encode(input_text, truncation=True, max_length=512)
            truncated_text = self.tokenizer.decode(tokens)

            # Generate response
            response = self.qa_chain.invoke({"query": truncated_text})
            
            return response['result'].strip()
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error while processing your question. Could you please try asking in a different way?"

def main():
    data_directory = input("Enter the path to your data directory (press Enter for default 'data'): ") or "data"
    model_name = input("Enter the model name (press Enter for default 'google/flan-t5-large'): ") or "google/flan-t5-large"

    print(f"Initializing chatbot with data from {data_directory} and model {model_name}")
    chatbot = RAGChatbot(data_directory, model_name)
    
    print("\nChatbot initialized. You can start asking questions.")
    print("Type 'quit' to exit the program.")

    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'quit':
            break
        response = chatbot.get_response(query)
        print(f"Response: {response}")

    print("Thank you for using the RAG Chatbot. Goodbye!")

if __name__ == "__main__":
    main()