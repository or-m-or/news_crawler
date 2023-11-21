import os
import openai
import logging
import sys
import nest_asyncio
from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
    LLMPredictor,
)
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.node_parser import SentenceSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index.response_synthesizers import TreeSummarize
from llama_index.llms import OpenAI

from config import config

from constants import (
    SUMMARY_PROMPT,
)




# openai.api_key = os.environ["OPENAI_API_KEY"]
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
nest_asyncio.apply()


# load data
# - input files path -> config
# - input file .txt 앞까지 리스트로 입력받기
def load_news_from_sample(input_directory_path) -> list:
    file_names = [f.split('.')[0] for f in os.listdir(input_directory_path) if f.endswith('.txt')]
    
    news_docs = []
    for file_name in file_names:
        docs = SimpleDirectoryReader(
            input_files=[f"{input_directory_path}/{file_name}.txt"]
        ).load_data()
        docs[0].doc_id = file_name
        news_docs.extend(docs)

    return news_docs



def initialize_doc_summary_index(config=config):
    llm_predictor = LLMPredictor(
        llm= OpenAI(
            temperature = config["llm_predictor"]["temperature"],
            model       = config["llm_predictor"]["model_name"],
        )
    )
    embedding = HuggingFaceEmbedding(
        model_name  = config["embed_model"]["model_name"],
    )

    # 문장 단위로 분리
    text_parser = SentenceSplitter(
        chunk_size=1024, # 한 청크에 포함될 수 있는 최대 문자 수
        # separator=" ",
    )
    # node_parser = SimpleNodeParser(text_splitter=text_splitter) 

    service_context = ServiceContext.from_defaults(
        llm_predictor = llm_predictor,
        embed_model   = embedding,
        node_parser   = text_parser, # 청크를 어떻게 노드로 분할할지 결정
        chunk_size    = 1024, # 한번에 처리할 텍스트의 최대 길이
        # prompt_helper
        # llama_logger
        # chunk_size_limit # 처리 가능한 최대 청크크기의 상한 선, chunk_size 보다 크거나 같아야 함.
    )
    print("complete init service_context")
    return service_context



def generate_summarize(documents:list, service_context):
    
    response_synthesizer = get_response_synthesizer(
        response_mode="compact", use_async=True
    )
    
    # 상세 설정 가능 
    # response_synthesizer = TreeSummarize(verbose=True, summary_template=SUMMARY_PROMPT) # 요약 스타일 지정 프롬프트

    index = DocumentSummaryIndex.from_documents(
        documents,
        service_context=service_context,
        response_synthesizer=response_synthesizer,
        show_progress=True,
    )

    summary_news_list = []
    for docs in documents:
        file_name = docs.doc_id
        summarized_news = index.get_document_summary(file_name) # 요약
        summary_news_list.extend(summarized_news)
        print("result : \n",summarized_news)



def save_summarized_file(summarized_result):
    document_folder = os.path.expanduser("~/documents/news_crawler/documents")
    folder_name = os.path.join(document_folder, "summary_results")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for summarized_news in summarized_result:
        file_name = f"{summarized_news.doc_id}_summary.txt"
        with open(os.path.join(folder_name, file_name), 'w', encoding='utf-8') as file:
            file.write(summarized_news)
    




if __name__ == "__main__":
    input_directory_path = r"C:\Users\thheo\Documents\news_crawler\sample"
    news_docs = load_news_from_sample(input_directory_path) # return list

    service_context = initialize_doc_summary_index()
    generate_summarize(news_docs, service_context)



