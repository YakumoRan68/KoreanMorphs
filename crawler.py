import requests
from bs4 import BeautifulSoup

req = requests.get("http://news.khan.co.kr/kh_news/khan_art_view.html?artid=201911050854001&code=940202")
html = req.text
soup = BeautifulSoup(fp, 'html.parser')

div = soup.find("content_text")
print(all_divs)