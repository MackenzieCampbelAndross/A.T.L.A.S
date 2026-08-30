import requests
from bs4 import BeautifulSoup

def search_web(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = [a.text for a in soup.find_all("a", class_="result__a")][:3]
    return " | ".join(results) if results else "No results found."
