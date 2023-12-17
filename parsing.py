import requests
from bs4 import BeautifulSoup

def parse(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        question = soup.find('div', class_='html_text').find_all('p')
        answers = soup.find('div', id='answer1').find_all('p')
        return question,answers