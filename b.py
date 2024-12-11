import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.ft.com/stream/7e37c19e-8fa3-439f-a870-b33f0520bcc0'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8',
    'Cache-Control': 'no-cache',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.select('div.o-teaser-collection.o-teaser-collection--stream > ul > li')

news_data = []
for article in articles:
    date = article.select_one('div.stream-card__date time')
    headline = article.select_one('div.o-teaser__meta a')
    title = article.select_one('div.o-teaser__heading a')
    summary = article.select_one('p.o-teaser__standfirst a')
    image = article.select_one('div.o-teaser__image-placeholder img')

    news_data.append({
        'Date': date['datetime'] if date else None,
        'Headline': headline.text.strip() if headline else None,
        'Title': title.text.strip() if title else None,
        'Summary': summary.text.strip() if summary else None,
        'Image': {
            'Src': image['data-src'],
            'Alt': image['alt']
        } if image else None
    })

news_df = pd.DataFrame(news_data)
news_df.to_csv('NewsData.csv', index=False)
print("Data saved to 'NewsData.csv'")