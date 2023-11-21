from llama_index import PromptTemplate


SUMMARY_PROMPT_TMPL = (
"""
Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge,
summarize the main points of the article in a concise manner. Then, translate the summary into Korean.

요약된 기사 : 
- [여기에 요약된 내용을 한국어로 번역합니다]
"""
)
SUMMARY_PROMPT = PromptTemplate(SUMMARY_PROMPT_TMPL)