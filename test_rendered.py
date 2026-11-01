
from bs4 import BeautifulSoup

with open("rendered_faq.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

answer = soup.find("p", class_="article-summary")

if answer:
    print(answer.get_text(" ", strip=True))
else:
    print("Answer not found")
