from bs4 import BeautifulSoup

with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    all_divs = soup.find_all("div")
    print(all_divs)