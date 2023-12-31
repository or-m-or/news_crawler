import sys
import os
from crawler import nytimes_crawler, news_summary


if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Too few arguments!")
        print("터미널에 'python crawler_usage.py <언론사 명> <뉴스 섹션> <뉴스 키워드> <크롤링할 뉴스 개수>'와 같이 기입해주세요")
    else:
        # 크롤링할 뉴스의 언론사 (nytimes, bloomberg)
        news_company = sys.argv[1]

        # 크롤링할 뉴스의 섹션
        # us, world, business, arts, lifestyle, opinion, technology, politics, business/economy, health 등 가능
        news_section = sys.argv[2]

        # 검색할 키워드
        news_query = sys.argv[3]

        # 크롤링할 뉴스의 개수 (단, news_count가 0일 때, 긁을 수 있는 모든 뉴스를 긁는다.)
        news_count = sys.argv[4]

        # 수정필요 : 저장할 때 언론사 추가하기
        if news_company == 'nytimes':
            news_docs = nytimes_crawler.crawling(news_section, news_query, news_count) # list
            news_summary.news_summarizer(news_docs)
        # elif news_company == 'bloomberg':
        #     news_docs = bloomberg_crawler.crawling(news_section, news_query, news_count) # list
        else:
            print(f"Error: '{news_company}'는 지원되지 않는 뉴스 회사입니다. 현재는 'nytimes' 및 'bloomberg'만 지원됩니다.")
            sys.exit(1)
        
        
        # news_summary.news_summarizer()