import tkinter as tk
from bs4 import BeautifulSoup
import requests, lxml

myQuery = ""

def mySetValue(entry, window):
    global myQuery
    myQuery = entry.get()
    window.destroy()

def launch():
    window = tk.Tk()
    label = tk.Label(text="Please enter your query below")
    entry = tk.Entry()
    button = tk.Button(
        text="Click here to submit",
        width=25,
        height=1,
        command=lambda: mySetValue(entry, window)
    )
    label.pack()
    entry.pack()
    button.pack()
    window.mainloop()
    myRequest()

def myRequest():
    data = []
    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.50"
    }
    html = requests.get(f'https://www.google.com/search?q={myQuery}', headers=headers)
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

def main():
    launch()
    exit(0)

if (__name__ == "__main__"):
    main()