"""
Document Summary Index useage
"""
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

# rebuild storage context
from llama_index.indices.loading import load_index_from_storage
from llama_index import StorageContext

# # LLM-based Retrieval
from llama_index.indices.document_summary import (
    DocumentSummaryIndexLLMRetriever,
)

# use retriever as part of a query engine
from llama_index.query_engine import RetrieverQueryEngine

# Embedding-based Retrieval
from llama_index.indices.document_summary import (
    DocumentSummaryIndexEmbeddingRetriever,
)

# use retriever as part of a query engine
from llama_index.query_engine import RetrieverQueryEngine




openai.api_key = os.environ["OPENAI_API_KEY"]

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
        input_files=[f"C:/Users/thheo/Documents/news_crawler/sample/{news_title}.txt"]
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
print("business_hamas_1의 요약 : \n")
print(doc_summary_index.get_document_summary("business_hamas_1"))

#------------------------------------------------------------------------

# # index2라는 이름으로 저장...?
doc_summary_index.storage_context.persist("index")
print("index 생성, 저장")


#------------------------------------------------------------------------
# 인덱스에 쿼리
print("----------High-level Querying----------")
# 1. 간단한 쿼리 처리
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="index")
doc_summary_index = load_index_from_storage(storage_context)

# Perform Retrieval from Document Summary Index
# High-level Querying
query_engine = doc_summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)
response = query_engine.query("What was the reaction of some Jewish screenwriters to the guild's silence") # 쿼리
print("query engine response : \n",response)

#------------------------------------------------------------------------
# 2
print("---------LLM-based Retrieval-----------")
# LLM-based Retrieval LLM 기반 검색
retriever = DocumentSummaryIndexLLMRetriever(
    doc_summary_index,
    # choice_select_prompt=None,
    # choice_batch_size=10,
    # choice_top_k=1,
    # format_node_batch_fn=None,
    # parse_choice_select_answer_fn=None,
    # service_context=None
)
retrieved_nodes = retriever.retrieve("What was the reaction of some Jewish screenwriters to the guild's silence") # 쿼리
# print("retrieved_nodes : \n", retrieved_nodes)
# print("노드 수 : ",len(retrieved_nodes)) # 노드 수
# print("노드 점수 : ",retrieved_nodes[0].score) # 노드 점수? 쿼리에 얼마나 부합하나..?
# print("노드 text : ",retrieved_nodes[0].node.get_text()) # 노드의 텍스트 정보



# use retriever as part of a query engine 쿼리 엔진을 통한 질의
# configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode="tree_summarize") # 응답 합성?

# assemble query engine LLM 기반 검색기 + 응답 합성기 결합하여 복잡한 쿼리 처리
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

# query
response = query_engine.query("What was the reaction of some Jewish screenwriters to the guild's silence")
print("query engine response : \n",response)


#------------------------------------------------------------------------
# 3. 문서의 임베딩을 사용하여 쿼리와 유사한 문서를 찾아내는 데 초점
print("---------Embedding-based Retrieval-----------")
# Embedding-based Retrieval
retriever = DocumentSummaryIndexEmbeddingRetriever(
    doc_summary_index,
    # similarity_top_k=1,
)
retrieved_nodes = retriever.retrieve("What was the reaction of some Jewish screenwriters to the guild's silence")
# print("retrieved nodes : \n",retrieved_nodes)
# print("노드 길이 : ",len(retrieved_nodes))
# print("노드 텍스트 : ",retrieved_nodes[0].node.get_text())


# use retriever as part of a query engine
# configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode="tree_summarize")

# assemble query engine 임베딩 기반 검색기 + 응답 합성기
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

# query
response = query_engine.query("What was the reaction of some Jewish screenwriters to the guild's silence")
print("query engine response : \n",response)