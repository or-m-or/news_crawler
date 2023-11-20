import os
import pytest
import openai
from setting import env

@pytest.fixture(scope='module')
def openai_api_key():
    os.environ["OPENAI_API_KEY"] = env('OPENAI_API_KEY')
    openai.api_key = os.environ["OPENAI_API_KEY"]
