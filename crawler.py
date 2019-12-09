import requests
import re
import datetime
import io
from time import sleep
from korea_news_crawler.articleparser import ArticleParser
from korea_news_crawler.articlecrawler import ArticleCrawler
from bs4 import BeautifulSoup

NOW = datetime.datetime.now()
FILE_NAME = f'{NOW.year}-{NOW.month:02d}-{NOW.day:02d}-{NOW.hour:02d}-{NOW.minute:02d}-{NOW.second:02d}'

def get_url_data(url, max_tries=10): #referenced from : https://github.com/lumyjuwon/KoreaNewsCrawler/blob/master/korea_news_crawler/articlecrawler.py
    remaining_tries = int(max_tries)
    while remaining_tries > 0:
        try:
            return requests.get(url)
        except requests.exceptions:
            sleep(60)
        remaining_tries = remaining_tries - 1
    raise ResponseTimeout()

ArticleParser.special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"◇※ⓒ©…△]')
ArticleParser.content_pattern = re.compile('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0|SUB TITLE START|SUB TITLE END|For Use Only in the Republic of Korea. No Redistribution|Yonhapnews|newsis.com|misocamera|ytn.co.kr|MobileAdNew center|yna.co.kr|nkphoto|photo|seephoto|bulls')

category = input("속보(001) 정치(100) 경제(101) 사회(102) 생활문화(103) 세계(104) IT과학(105) 오피니언(110)\n카테고리 입력 : ")
y1, y2, m1, m2 = map(int, input("년(시작), 년(끝), 월(시작), 월(끝) 입력 : ").split())
NEWS_LIST_URL = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + category + "&date="

print(f"Make news list URL from {y1}-{m1:02d} to {y2}-{m2:02d}")
NEWS_LIST_URL_BY_DATE = ArticleCrawler().make_news_page_url(NEWS_LIST_URL, y1, y2, m1, m2)

with io.open(FILE_NAME, 'w+', encoding = 'utf-8') as output :
    print("Create file " + FILE_NAME + ", start crawling...")
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
            post.append(line.a.get('href')) # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
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

                output.write(text_sentence)

            except Exception as ex:
                del request_content, document_content
                pass