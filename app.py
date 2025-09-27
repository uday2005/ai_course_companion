from llama_index.core import SimpleDirectoryReader 
from llama_index.core.schema import Document

import os
from dotenv import load_dotenv
from llama_index.core import  Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.extractors import TitleExtractor
from llama_index.llms.gemini import Gemini

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# So i am using the ollama not gemini  earlier i was thinking to use gemini but it was hiting rate limit
Settings.embed_model = OllamaEmbedding(
    model_name="llama3", 
    base_url="http://localhost:11434"  # default Ollama endpoint
)

Settings.llm = Ollama(
    model="mistral",
    request_timeout=60.0,
    context_window=8000,
)

# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Settings.embed_model = GeminiEmbedding(
#     api_key=GOOGLE_API_KEY,
#     model_name="models/embedding-001"
# )
# Settings.llm = Gemini(api_key=GOOGLE_API_KEY, model="gemini-2.5-pro")

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext



book_db = chromadb.PersistentClient(path="./storage_book")
book_collection = book_db.get_or_create_collection("book")
book_vector_store = ChromaVectorStore(chroma_collection=book_collection)
BookStorageContext = StorageContext.from_defaults(vector_store=book_vector_store)
book_index = VectorStoreIndex.from_vector_store(
    book_vector_store, storage_context=BookStorageContext
)


transcript_db = chromadb.PersistentClient(path="./storage_transcripts")
transcript_collection = transcript_db.get_or_create_collection("transcripts")
transcript_vector_store = ChromaVectorStore(chroma_collection=transcript_collection)
TranscriptStorageContext = StorageContext.from_defaults(vector_store=transcript_vector_store)
transcript_index = VectorStoreIndex.from_vector_store(
    transcript_vector_store ,storage_context= TranscriptStorageContext
)


from llama_index.core import VectorStoreIndex , get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


#  I will use retriever later as it is more strict in searcing it will give more accuarte information
# but when it will not find teh relevat information it will not give any answers , it is so strict.

# retriever = VectorIndexRetriever(
#     index=book_index,
#     similarity_top_k=10,
# )

# # configure response synthesizer
# response_synthesizer = get_response_synthesizer()

# query_engine = RetrieverQueryEngine(
#     retriever=retriever,
#     response_synthesizer=response_synthesizer,
#     node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)]

# )
book_query_engine = book_index.as_query_engine(response_mode="compact")  # or "tree_summarize"
# book_response = book_query_engine.query("What is the definition of learning rate")
# print(book_response)

transcript_query_engine = transcript_index.as_query_engine(response_mode="compact")
# transcript_response = transcript_query_engine.query("what is the learning rate")
# print(transcript_response)


from llama_index.core.tools import QueryEngineTool

book_tool = QueryEngineTool.from_defaults(
    book_query_engine ,
    name='fastai_textbook_retriever',
     description=(
        "Use this tool to answer questions about the theory, concepts, definitions, "
        "and in-depth explanations from the official fast.ai textbook. "
        "It is the best source for foundational knowledge and 'why' questions."
    )
)

transcript_tool = QueryEngineTool.from_defaults(
    query_engine=transcript_query_engine,
    name="lecture_transcript_retriever",
    description=(
        "Use this tool to find specific examples, practical advice, or direct quotes "
        "mentioned by the instructor, Jeremy Howard, in the video lectures. "
        "This tool is best for 'how-to' questions or finding specific implementation details that were spoken about."
    )
)

tools = [book_tool , transcript_tool]

from llama_index.core.agent.workflow import AgentWorkflow

agent = AgentWorkflow.from_tools_or_functions(
    tools,
    llm = Settings.llm,
    verbose=True,
)


import asyncio

async def main():

    response = await agent.run("What is a loss function? Use the textbook to answer.")
    
    print("\n--- Final Agent Response ---")
    print(response)

    # Now try a more complex, multi-tool question
    print("\n--- Running a multi-tool query ---")
    response_multi = await agent.run(
        "First, use the textbook to define transfer learning. "
        "Then, use the lecture transcripts to find out what Jeremy Howard says about its importance."
    )
    print("\n--- Final Agent Response (Multi-Tool) ---")
    print(response_multi)

if __name__ == "__main__":
    asyncio.run(main())