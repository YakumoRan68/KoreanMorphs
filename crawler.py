import requests
import re
from time import sleep
from korea_news_crawler.articleparser import ArticleParser
from korea_news_crawler.articlecrawler import ArticleCrawler
from bs4 import BeautifulSoup

category = "001" #속보
NEWS_LIST_URL = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + category + "&date="
NEWS_LIST_URL_BY_DATE = ArticleCrawler().make_news_page_url(NEWS_LIST_URL, 2019, 2019, 11, 11)

def get_url_data(url, max_tries=10): #referenced from : https://github.com/lumyjuwon/KoreaNewsCrawler/blob/master/korea_news_crawler/articlecrawler.py
    remaining_tries = int(max_tries)
    while remaining_tries > 0:
        try:
            return requests.get(url)
        except requests.exceptions:
            sleep(60)
        remaining_tries = remaining_tries - 1
    raise ResponseTimeout()

for URL in NEWS_LIST_URL_BY_DATE : #referenced from : https://github.com/lumyjuwon/KoreaNewsCrawler/blob/master/korea_news_crawler/articlecrawler.py
    regex = re.compile("date=(\d+)")
    news_date = regex.findall(URL)[0]
    request = get_url_data(URL)
    document = BeautifulSoup(request.content, 'html.parser')

    # html - newsflash_body - type06_headline, type06
    # 각 페이지에 있는 기사들 가져오기
    post_temp = document.select('.newsflash_body .type06_headline li dl')
    post_temp.extend(document.select('.newsflash_body .type06 li dl'))

    post = []
    MAXCOUNT = 0
    for line in post_temp:
        if MAXCOUNT >= 10 :
            break
        post.append(line.a.get('href')) # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
        MAXCOUNT += 1
    del post_temp
    
    MAXCOUNT = 0
    for content_url in post:  # 기사 URL
        if MAXCOUNT >= 1 :
            break
        # 크롤링 대기 시간
        sleep(0.01)
        
        # 기사 HTML 가져옴
        request_content = get_url_data(content_url)
        try:
            document_content = BeautifulSoup(request_content.content, 'html.parser')
        except:
            continue

        try:
            text_sentence = ""

            tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
            text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
            if not text_sentence:  # 공백일 경우 기사 제외 처리
                continue

            print(text_sentence)

        except Exception as ex:
            del request_content, document_content
            pass

