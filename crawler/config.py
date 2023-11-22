config = {
    "llm_predictor": 
    {
        "model_name" : "gpt-3.5-turbo-1106",
        "temperature": 0,
    },
    "embed_model": 
    {
        "model_name": "intfloat/e5-small",
        "cache_dir" : r"C:\Users\thheo\Documents\crawler_test\embedding_model",
    },

    "default_input_directory": r".\documents\crawling_results",
}


# gpt-3.5-turbo-1106
#   context window : 16,385 tokens
#   output tokens : maximum 4,096 tokens