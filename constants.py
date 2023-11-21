from llama_index import PromptTemplate


SUMMARY_PROMPT_TMPL = (
"""
Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge,
"""
)
SUMMARY_PROMPT = PromptTemplate(SUMMARY_PROMPT_TMPL)