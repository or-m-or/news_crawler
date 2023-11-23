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
from llama_index.schema import Document


openai.api_key = os.environ["OPENAI_API_KEY"]
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
nest_asyncio.apply()


def generate_news_summeries(news_docs, config=config):
    """ 뉴스 기사의 요약 및 번역을 수행하는 함수 """
    
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
        # chunk_size    = 1024,        # 한번에 처리할 텍스트의 최대 길이
        )
    response_synthesizer = TreeSummarize(
        verbose=True, 
        summary_template=SUMMARY_PROMPT
    ) 

    documents = [Document(doc_id=item["doc_id"], text=item["title"]+'\n'+item["content"]) for item in news_docs]
    
    index = DocumentSummaryIndex.from_documents(
        documents,
        service_context=service_context,
        response_synthesizer=response_synthesizer,
        show_progress=True,
    )

    # 기사 요약
    for item in news_docs:
        news_summary = index.get_document_summary(item['doc_id'])
        item["summary"] = news_summary
        # print("news_summary :\n",news_summary)

    return news_docs
    


def save_news_summary(documents, output_directory_path):
    """ 요약 및 번역한 뉴스 기사 CSV로 저장하는 함수 """

    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"{documents[0]['section']}_{documents[0]['query']}_{current_time}"
    hash_file_name = hashlib.md5(file_name.encode()).hexdigest()
    output_file_name = f"{hash_file_name}.csv"
    output_file_path = os.path.join(output_directory_path, output_file_name)

    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'author', 'date', 'summary', 'content'])

        for doc in documents:
            title = doc['title']
            author = doc['author']
            date = doc['date']
            summary = doc['summary']
            content = doc['content']
            writer.writerow([title, author, date, summary, content])



def news_summarizer(news_docs):
    start_time = time.time()
    # input_directory_path = r"C:\Users\thheo\Documents\news_crawler\documents\crawling_results"
    output_directory_path = r"C:\Users\thheo\Documents\news_crawler\documents\summary_results"    
    
    # news_docs = load_news(input_directory_path)
    news_docs_with_summaries = generate_news_summeries(news_docs) # list
    save_news_summary(news_docs_with_summaries, output_directory_path)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"news_summarizer 실행 시간: {total_time}초")



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
