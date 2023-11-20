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



openai.api_key = os.environ["OPENAI_API_KEY"]

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

nest_asyncio.apply() 
# 비동기 IO 작업을 중첩하여 사용할 수 있게 함. 
# (동일한 스레드 내에서 여러 이벤트 루프 중첩해여 사용)

# load data
news_docs = []
docs = SimpleDirectoryReader(
    input_files=[r"sample\business_hamas_1_1117_150040.txt"]
).load_data()
news_docs.extend(docs)


# LLM
chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=chatgpt, chunk_size=1024)

# Index default mode
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
)
doc_summary_index = DocumentSummaryIndex.from_documents(
    news_docs,
    service_context=service_context,
    response_synthesizer=response_synthesizer,
    show_progress=True,
)





