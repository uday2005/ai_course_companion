from llama_index.core import SimpleDirectoryReader 

print("Loading textbook ")
book_reader = SimpleDirectoryReader("./data/book")
book_documents = book_reader.load_data()

print("Loading notebooks")
notebook_reader = SimpleDirectoryReader("./data/notebooks")
notebook_documents = notebook_reader.load_data()

print("Loading Transcripts")
transcripts_reader = SimpleDirectoryReader("./data/transcripts")
transcripts_documents = transcripts_reader.load_data()

from llama_index.core.schema import Document

def clean_text(text):
    return text.encode("utf-8", "replace").decode("utf-8")

def clean_documents(documents):
    cleaned_docs = []
    for doc in documents:
        if hasattr(doc, "text"):
            cleaned_text = clean_text(doc.text)
            # Create a new Document with the cleaned text and preserve metadata
            cleaned_docs.append(Document(text=cleaned_text, metadata=getattr(doc, "metadata", {})))
        else:
            cleaned_docs.append(doc)
    return cleaned_docs

book_documents = clean_documents(book_documents)
transcripts_documents = clean_documents(transcripts_documents)
notebook_documents = clean_documents(notebook_documents)



import os
from dotenv import load_dotenv
from llama_index.core import  Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.extractors import TitleExtractor
from llama_index.llms.gemini import Gemini

load_dotenv()


# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Settings.embed_model = GeminiEmbedding(api_key=GOOGLE_API_KEY,model_name="models/embedding-001")
# Settings.llm = Gemini(api_key=GOOGLE_API_KEY, model="gemini-2.5-pro")

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.embed_model = OllamaEmbedding(
    model_name="llama3",  # or another supported model
    base_url="http://localhost:11434"  # default Ollama endpoint
)
Settings.llm2 = Ollama(
    model="llama3",
    request_timeout=60.0,
    context_window=8000,
)



pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1024 , chunk_overlap=20),
        Settings.embed_model 
    ]
)

transcripts_node = pipeline.run(documents =transcripts_documents)
notebook_node = pipeline.run(documents =notebook_documents)
book_nodes = pipeline.run(documents =book_documents)


import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext


# intiialize client , setting path to save data
book_db = chromadb.PersistentClient(path="./storage_book")

# create collection
book_collection = book_db.get_or_create_collection("book")


# assign chroma as the vector_store to the context
book_vector_store = ChromaVectorStore(chroma_collection=book_collection)
BookStorageContext = StorageContext.from_defaults(vector_store=book_vector_store)


# Create the persistent client for the TRANSCRIPTS
transcript_db = chromadb.PersistentClient(path="./storage_transcripts")

# Create the collection for the TRANSCRIPTS
transcript_collection = transcript_db.get_or_create_collection("transcripts")

# Create the adapter for the TRANSCRIPTS
transcript_vector_store = ChromaVectorStore(chroma_collection=transcript_collection)

# Create the storage context for the TRANSCRIPTS
TranscriptStorageContext = StorageContext.from_defaults(vector_store=transcript_vector_store)


# same for the notebook
notebook_db = chromadb.PersistentClient(path="./storage_notebooks")
notebook_collection = notebook_db.get_or_create_collection("notebooks")
notebook_vector_store = ChromaVectorStore(chroma_collection=notebook_collection)
NotebookStorageContext = StorageContext.from_defaults(vector_store=notebook_vector_store)

book_index = VectorStoreIndex(
    nodes=book_nodes, storage_context=BookStorageContext
)

transcript_index = VectorStoreIndex(
    nodes=transcripts_node, storage_context=TranscriptStorageContext
)

notebook_index = VectorStoreIndex(
    nodes=notebook_node, storage_context=NotebookStorageContext
)