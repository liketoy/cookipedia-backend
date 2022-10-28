import requests
from bs4 import BeautifulSoup

headers = {
    "referer": "https://sauce.foodpolis.kr/home/specialty/foodDbSearch.do",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36",
}
url = "https://sauce.foodpolis.kr/home/specialty/foodDbSearch.do?PAGE_MN_ID=SIS-030101"


req = requests.post(url, headers=headers)

soup = BeautifulSoup(req.text, "html.parser")

ingredients = soup.select(
    "#content > div.boardGroup > div.conTableGroup.MAB30 > table > tbody > tr"
)

# content > div.boardGroup > div.conTableGroup.MAB30 > table > tbody > tr:nth-child(1) > td:nth-child(2) > a
# content > div.boardGroup > div.conTableGroup.MAB30 > table > tbody > tr:nth-child(2) > td:nth-child(2) > a
# content > div.boardGroup > div.conTableGroup.MAB30 > table > tbody > tr:nth-child(1) > td.m

for ingredient in ingredients:
    a = ingredient.select_one("td:nth-child(2) > a")
    num = ingredient.select_one("td.m")
    ingredient_title = a.text
    num = num.text
    print(num, ingredient_title)
