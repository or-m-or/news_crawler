import pytest

from langchain.chat_models import ChatOpenAI
from llama_index import ServiceContext, LLMPredictor, Document
from llama_index.node_parser import SimpleNodeParser
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index import (
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    Document,
    get_response_synthesizer,
    ListIndex
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader(r"C:\Users\thheo\Documents\crawler_test\documents\crawling_results").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("Summarize in one sentence")
print(response)


def initialize_index():
    


