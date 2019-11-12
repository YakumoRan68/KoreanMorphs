import requests
import re
from bs4 import BeautifulSoup

special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]')
content_pattern = re.compile('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0')

def clear_content(cls, text) :
    newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
    special_symbol_removed_content = re.sub(cls.special_symbol, ' ', newline_symbol_removed_text)
    end_phrase_removed_content = re.sub(cls.content_pattern, '', special_symbol_removed_content)
    blank_removed_content = re.sub(' +', ' ', end_phrase_removed_content).lstrip()  # 공백 에러 삭제
    reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse 한다.
    content = ''
    for i in range(0, len(blank_removed_content)):
        # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지움
        if reversed_content[i:i + 2] == '.다':
            content = ''.join(reversed(reversed_content[i:]))
            break

    return content


postfix = "001&oid=014&aid=0004325780"
url = "https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=" + postfix
req = requests.get(url)
html = req.content
soup = BeautifulSoup(html, 'html.parser')
div = soup.find_all('div', {'id': 'articleBodyContents'})

text_sentence + clear_content(str(div[0].find_all(text=True)))

print(div)
