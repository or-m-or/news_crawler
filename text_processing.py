import os
import openai

from llama_index.llms import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import config

from llama_index import (
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    Document,
)

import threading

# os.environ["OPENAI_API_KEY"] = api_key
# openai.api_key = os.environ["OPENAI_API_KEY"]

def service_context_from_config(config=config):
    llm_predictor = LLMPredictor(
        llm= OpenAI(
            temperature= config["llm_predictor"]["temperature"],
            model      = config["llm_predictor"]["model_name"]
        )
    )
    embedding = HuggingFaceEmbedding(
        model_name  = config["embed_model"]["model_name"],
        cache_folder= config["embed_model"]["cashe_dir"], 
    )
    text_splitter =
    node_parser = 
    service_context = ServiceContext.from_defaults(
        llm_predictor= llm_predictor,
        embed_model  = embedding,
        # node_parser=node_parser
    )
    return service_context


class KoreanSummaryGenerator:
    def __init__(self, document_text):
        self.service_context = service_context_from_config()
        # self.nodes = self.service_context.node_parser.get_nodes_from_documents([Document(text=document_text)])
        # self.query_engines, self.node_list = self.initialize_query_engines()
        # self.pattern = re.compile(r'[QA]:\s*')
        self.lock = threading.Lock()
        self.gen_faqs = [[], []]
        self.open_ended, self.m_choices = 0, 1





def processing(input_file: str):
    documents = SimpleDirectoryReader(input_files=[input_file]).load_data()
    document_text = "".join([doc.get_text() for doc in documents])

    result = KoreanSummaryGenerator(document_text=document_text)

    return 