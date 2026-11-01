from bs4 import BeautifulSoup

with open("html_doc.html", "r", encoding="utf-8") as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())

