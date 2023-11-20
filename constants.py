from llama_index.prompts.prompts import QuestionAnswerPrompt


SUMM_TRAN_TMPL = (
    """
Context information is below.
---------------------
{context_str}
---------------------
Summarize and translate the contents of the context into Korean
"""
)