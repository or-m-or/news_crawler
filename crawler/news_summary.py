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

from crawler.config import config
import csv

from crawler.constants import (
    SUMMARY_PROMPT,
)
from datetime import datetime
import time
import hashlib


openai.api_key = os.environ["OPENAI_API_KEY"]
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
nest_asyncio.apply()

# 클래스로 만들기


# def load_news(input_directory_path) -> list:
#     file_names = [f.split('.')[0] for f in os.listdir(input_directory_path) if f.endswith('.txt')]
    
#     news_docs = []
#     for file_name in file_names:
#         reader = SimpleDirectoryReader(input_files=[f"{input_directory_path}/{file_name}.txt"])
#         docs = reader.load_data()
#         docs[0].doc_id = file_name
#         docs[0].hash = hash(reader)  # SimpleDirectoryReader 객체의 해시값을 저장
#         news_docs.extend(docs)
#     return news_docs



# index 만드는거를 분리 하지말고, 요약 생성하는 기능, 파일 저장하는 기능 완전히 분리
# service_comtext 초기화
# def initialize_index(documents, config=config):
#     llm_predictor = LLMPredictor(
#         llm= OpenAI(
#             temperature = config["llm_predictor"]["temperature"],
#             model       = config["llm_predictor"]["model_name"],
#         )
#     )
#     embedding = HuggingFaceEmbedding(
#         model_name  = config["embed_model"]["model_name"],
#     )

#     # # 문장 단위로 분리
#     # text_parser = SentenceSplitter(
#     #     chunk_size=1024, # 한 청크에 포함될 수 있는 최대 문자 수
#     #     # separator=" ",
#     # )

#     service_context = ServiceContext.from_defaults(
#         llm_predictor = llm_predictor,
#         embed_model   = embedding,
#         # node_parser   = text_parser, # 청크를 어떻게 노드로 분할할지 결정
#         # chunk_size    = 1024, # 한번에 처리할 텍스트의 최대 길이
        
#         # prompt_helper
#         # llama_logger
#         # chunk_size_limit # 처리 가능한 최대 청크크기의 상한 선, chunk_size 보다 크거나 같아야 함.
#     )

#     # response_synthesizer를 만드는 다른 방법
#     # response_synthesizer = get_response_synthesizer(
#     #     response_mode="compact", use_async=True
#     # )
#     response_synthesizer = TreeSummarize(verbose=True, summary_template=SUMMARY_PROMPT) 
#     index = DocumentSummaryIndex.from_documents(
#         documents,
#         service_context=service_context,
#         response_synthesizer=response_synthesizer,
#         show_progress=True,
#     )
#     return index






def generate_summeries(scraplist, config=config):
    llm_predictor = LLMPredictor(
        llm= OpenAI(
            temperature = config["llm_predictor"]["temperature"],
            model       = config["llm_predictor"]["model_name"],
        )
    )
    embedding = HuggingFaceEmbedding(
        model_name  = config["embed_model"]["model_name"],
    )
    # text_parser = SentenceSplitter(
    #     chunk_size=1024, # 한 청크에 포함될 수 있는 최대 문자 수
    #     # separator=" ",
    # )

    service_context = ServiceContext.from_defaults(
        llm_predictor = llm_predictor,
        embed_model   = embedding,
        # node_parser   = text_parser, # 청크를 어떻게 노드로 분할할지 결정
        # chunk_size    = 1024, # 한번에 처리할 텍스트의 최대 길이
        
        # prompt_helper
        # llama_logger
        # chunk_size_limit # 처리 가능한 최대 청크크기의 상한 선, chunk_size 보다 크거나 같아야 함.
    )
    response_synthesizer = TreeSummarize(verbose=True, summary_template=SUMMARY_PROMPT) 
    index = DocumentSummaryIndex.from_documents(
        scraplist,
        service_context=service_context,
        response_synthesizer=response_synthesizer,
        show_progress=True,
    )

    for scrapdata in scraplist:
        scrapdata.doc_id = hash(scraplist[0].title)
        news_summary = index.get_document_summary(scrapdata.doc_id)
        scrapdata.news_summary = news_summary
    
    return scraplist # 기존 scraplist + doc_id, news_summary


def save_news_summary(scraplist, output_directory_path):
    ...




def save_summaries(documents:list, index, output_directory_path):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{current_time}"
    hashed_file_name = hashlib.md5(output_file_name.encode()).hexdigest()

    output_file_name = f"{hashed_file_name}.csv"
    output_file_path = os.path.join(output_directory_path, output_file_name)

    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['doc_id','news_summary'])  # CSV 파일의 헤더

        for doc in documents:
            # start_time = time.time()
            file_name = doc.doc_id
            news_summary = index.get_document_summary(file_name)
            writer.writerow([file_name, news_summary])

            # end_time = time.time()
            # total_time = end_time - start_time
            # print(f"뉴스 요약 중...{index+1}/{len(documents)} - 실행 시간: {total_time}초")
            # print(news_summary)




def news_summarizer(scraplist: list):
    start_time = time.time()
    input_directory_path = r"C:\Users\thheo\Documents\news_crawler\documents\crawling_results"
    output_directory_path = r"C:\Users\thheo\Documents\news_crawler\documents\summary_results"


    generate_summeries(scraplist)

        

    # news_docs = load_news(input_directory_path) # return list
    # index = initialize_index(news_docs)
    # save_summaries(news_docs, index, output_directory_path)

    end_time = time.time()  # 종료 시간 기록
    total_time = end_time - start_time  # 총 실행 시간 계산
    print(f"news_summarizer 실행 시간: {total_time}초")


if __name__ == "__main__":
    news_summarizer()

