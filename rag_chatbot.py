import json
from typing import List
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
)
from langchain_huggingface import HuggingFacePipeline

class RAGChatbot:
    def __init__(self, data_directory: str, model_name: str = "google/flan-t5-base"):
        self.model_name = model_name
        self.embeddings = HuggingFaceEmbeddings()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vectorstore = None
        self.qa_chain = None

        self.documents = self.load_documents(data_directory)
        self._setup()

    def load_documents(self, directory: str) -> List[Document]:
        documents = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filename.endswith('.txt'):
                loader = TextLoader(filepath)
                documents.extend(loader.load())
            elif filename.endswith('.pdf'):
                loader = PyPDFLoader(filepath)
                documents.extend(loader.load())
            elif filename.endswith('.json'):
                documents.extend(self.load_json(filepath))
            elif filename.endswith('.csv'):
                loader = CSVLoader(filepath)
                documents.extend(loader.load())
            elif filename.endswith('.html'):
                loader = UnstructuredHTMLLoader(filepath)
                documents.extend(loader.load())
            elif filename.endswith('.md'):
                loader = UnstructuredMarkdownLoader(filepath)
                documents.extend(loader.load())
            else:
                print(f"Unsupported file type: {filename}")
        
        return documents

    def load_json(self, filepath: str) -> List[Document]:
        with open(filepath, 'r') as file:
            data = json.load(file)
        
        documents = []
        if isinstance(data, dict):
            for key, value in data.items():
                documents.append(Document(page_content=f"{key}: {value}"))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    documents.append(Document(page_content=json.dumps(item)))
                else:
                    documents.append(Document(page_content=str(item)))
        
        return documents

    def _setup(self):
        texts = [doc.page_content for doc in self.documents]
        split_texts = self.text_splitter.split_text("\n\n".join(texts))

        self.vectorstore = Chroma.from_texts(split_texts, self.embeddings, persist_directory="./chroma_db")

        llm = HuggingFacePipeline(pipeline=pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer, max_length=512))
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )

    def get_response(self, query: str) -> str:
        response = self.qa_chain({"query": query})
        return response['result']

def main():
    print("Initializing RAG Chatbot...")
    chatbot = RAGChatbot("./data")
    print("Chatbot initialized. You can start asking questions.")
    print("Type 'quit' to exit.")
    
    while True:
        query = input("\nYour question: ")
        if query.lower() == 'quit':
            break
        response = chatbot.get_response(query)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()