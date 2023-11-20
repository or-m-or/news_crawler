import os
import openai

from llama_index.llms import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.indices.document_summary import DocumentSummaryIndex
# from llama_index.text_splitter import SentenceSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import config

from llama_index import (
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    Document,
    LangchainEmbedding,
    get_response_synthesizer,
    ListIndex
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import MetadataMode

from typing import (
    Optional,
    List, 
    Dict,
)

from constants import(
    SUMM_TRAN_TMPL
)


def init_service_context(config=config):
    llm_predictor = LLMPredictor(
        llm= OpenAI(
            temperature= config["llm_predictor"]["temperature"],
            model      = config["llm_predictor"]["model_name"],
        )
    )
    hf = HuggingFaceEmbeddings(model_name  =config["embed_model"]["model_name"],
                               cache_folder=config["embed_model"]["cache_dir"],
                               model_kwargs={'device': 'cpu'})
    
    embedding = LangchainEmbedding(hf)
    # embedding = HuggingFaceEmbedding(
    #     model_name  = config["embed_model"]["model_name"],
    #     cache_folder= config["embed_model"]["cashe_dir"], 
    # )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024) # chunk_overlap=
    node_parser = SimpleNodeParser(text_splitter=text_splitter)
    service_context = ServiceContext.from_defaults(
        llm_predictor= llm_predictor,
        embed_model  = embedding,
        node_parser=node_parser
    )

    return service_context

# 임시 테스트 함수
def gpt_test(service_context):
    index = ListIndex.from_documents([Document(text=self.document_text)])

    query_engine = index.as_query_engine(
        service_context=self.service_context,
        query_template=SUMM_TRAN_TMPL,
        streaming=True
    )
    response = query_engine.query("")
    
    return response


class NewsSummaryAndTranslation:
    def __init__(self, document_text):
        self.service_context = init_service_context()
        self.nodes = self.service_context.node_parser.get_nodes_from_documents([Document(text=document_text)]) #?
        self.query_engines, self.node_list = self.initialize_query_engines()


        self.document_text = document_text # 임시


        # self.nodes = self.service_context.node_parser.get_nodes_from_documents([Document(text=document_text)])
        # self.query_engines, self.node_list = self.initialize_query_engines()



    # def initialize_query_engines(self) -> List:
    #     query_engine_per_node = []
    #     node_list = []
    #     for node in self.nodes:
    #         text = node.get_content(metadata_mode=MetadataMode.NONE).strip()
    #         index = ListIndex.from_documents(
    #             [ Document(text=text) ]
    #         )
    #         query_engine = index.as_query_engine(service_context=self.service_context,
    #                                              text_qa_template=SUMM_TRAN_TMPL,
    #                                              streaming=True)
            
    #         query_engine_per_node.append(query_engine)
    #         node_list.append(text)

    #     print(f"Number of nodes: {len(self.nodes)} | Success: Initialize query engines.")
    #     return query_engine_per_node, node_list
    

    # def generate_summarize_list(
            
    # )







# 입력 : 크롤링한 '파일' 경로
def app_process_news(input_file: str):
    documents = SimpleDirectoryReader(input_files=[input_file]).load_data()
    document_text = "".join([doc.get_text() for doc in documents]) 
    

    news_processor = NewsSummaryAndTranslation(document_text=document_text)
    result = news_processor.summarize_and_translate()
    # query_engines, node_list = news_processor.initialize_query_engines()
    # summary_results = news_processor.summarize_and_translate(query_engines, node_list)
    
    return result



if __name__=="__main__":
    input_file = r"C:\Users\thheo\Documents\crawler_test\documents\crawling_results_business_hamas_1117\business_hamas_1_1117_150112.txt"  # 입력 파일 경로 지정
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    if openai.api_key:
        
        results = app_process_news(input_file)
        print(f"results : \n",results)
    else :
        print("no api key")