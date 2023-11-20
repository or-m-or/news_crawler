import os
import openai
import logging
import sys
import nest_asyncio
from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
)
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.llms import OpenAI
from llama_index.indices.loading import load_index_from_storage
from llama_index import StorageContext


# openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = "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"

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

nest_asyncio.apply() 
# 비동기 IO 작업을 중첩하여 사용할 수 있게 함. 
# (동일한 스레드 내에서 여러 이벤트 루프 중첩해여 사용)

# load data
news_titles = ["business_hamas_1"] # ,business_hamas_2, ...
news_docs = []
for news_title in news_titles:
    docs = SimpleDirectoryReader(
        input_files=[f"sample/{news_title}.txt"]
    ).load_data()
    docs[0].doc_id = news_title
    news_docs.extend(docs)


# LLM
chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=chatgpt, chunk_size=1024)

# default mode of building the index
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
)
doc_summary_index = DocumentSummaryIndex.from_documents(
    news_docs,
    service_context=service_context,
    response_synthesizer=response_synthesizer,
    show_progress=True,
)


# business_hamas_1 에 대한 요약
print(doc_summary_index.get_document_summary("business_hamas_1"))

doc_summary_index.storage_context.persist("index")

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="index")
doc_summary_index = load_index_from_storage(storage_context)


# Perform Retrieval from Document Summary Index
# High-level Querying
query_engine = doc_summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)
response = query_engine.query("say korean")
print(response)