import requests
import AlexPart.myConfig as myConfig
from bs4 import BeautifulSoup

def myRequest():
    data = []
    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.50"
    }
    html = requests.get(f'https://www.google.com/search?q={myConfig.myQuery}', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    for result in soup.select('.tF2Cxc'):
        title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
        displayed_link = result.select_one('.TbwUpd.NJjxre').text
        try:
            snippet = result.select_one('#rso .lyLwlc').text
        except:
            snippet = None
        print(f'{title}\n{link}\n{displayed_link}\n{snippet}\n')
        data.append({
            'title': title,
            'link': link,
            'displayed link': displayed_link,
            'snippet': snippet
        })