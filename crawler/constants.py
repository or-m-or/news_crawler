from llama_index import PromptTemplate


SUMMARY_PROMPT_TMPL = (
"""
Context:
News Article Text:
---------------------
{context_str}
---------------------

Task:
Summarize the contents of a news article by focusing on the article title, and then submit the translated summary in Korean.

Output:
[The translated summary will be provided here]
"""
)
SUMMARY_PROMPT = PromptTemplate(SUMMARY_PROMPT_TMPL)