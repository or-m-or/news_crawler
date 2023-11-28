config = {
    "llm_predictor": 
    {
        'model_name' : 'gpt-3.5-turbo-1106',
        'temperature': 0,
    },
    "embed_model": 
    {
        'model_name': 'intfloat/e5-small',
        'cache_dir' : r'C:\Users\thheo\Documents\crawler_test\embedding_model',
    },
    "path":
    {
        'chromedriver'   : r'C:\Users\thheo\Documents\news_crawler\chromedriver.exe',
        'input_directory': r'.\documents\crawling_results',
    },
    "nytimes":
    {
        'login_email'         : '',
        'login_password'      : '',
        'login_email_input'   : '//*[@id="myAccountAuth"]/div/div/div/form/div/div[4]/button',
        'login_password_input': '//*[@id="myAccountAuth"]/div/div/form/div/div[2]/button',
        'account_url'         : r'https://www.nytimes.com/account',
        'login_url'           : r'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=acct&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Faccount',
        'article_section_url' : r'https://www.nytimes.com/section/',
        # 'article_css'         : 'li[data-testid="search-bodega-result"]',
    },
    "nytimes_header":
    {
        'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept'         : 'application/json',
        'Origin'         : r'https://myaccount.nytimes.com',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type'   : 'application/json',
        'Referer'        : r'https://myaccount.nytimes.com/auth/login?response_type=cookie&client_id=vi&redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fsubscription%2Fonboarding-offer%3FcampaignId%3D7JFJX%26EXIT_URI%3Dhttps%253A%252F%252Fwww.nytimes.com%252F&asset=masthead',
    },
}
