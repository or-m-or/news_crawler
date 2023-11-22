import sys
import os
from crawler import nytimes_crawler, news_summary


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Too few arguments!")
        print("python crawler_usage.py <news_section> <news_query> <number-of-documents-to-crawling>")
    else:
        # 크롤링할 뉴스의 섹션
        # 뉴욕타임스의 섹션 종류 
        # : Any, Arts, Books, Business, New York, Opinion, Sports, Style, U.S., World, politics, Health, Tech, Science, etc...
        news_section = sys.argv[1]

        # 검색할 키워드
        news_query = sys.argv[2]

        # 크롤링할 뉴스의 개수
        # news_count가 0일 때, 긁을 수 있는 모든 뉴스를 긁는다.
        news_count = sys.argv[3]

        # nytimes_crawler.crawling(news_section, news_query, news_count)
        news_summary.news_summarizer()