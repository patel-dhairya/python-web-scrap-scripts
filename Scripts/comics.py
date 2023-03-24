# installation required with pip - aiohttp, bs4

import asyncio
import aiohttp
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()

async def scrape_link(link):
    link_html = await fetch(link)
    link_soup = BeautifulSoup(link_html, 'html.parser')
    fwd_element = int(link_soup.find(class_="bmc").text.split()[2])
    return fwd_element

async def main():
    url = 'https://www.asurascans.com/manga/list-mode/'
    main_html = await fetch(url)
    main_soup = BeautifulSoup(main_html, 'html.parser')
    series_elements = main_soup.find_all(class_='series')

    tasks = []
    for element in series_elements:
        link_url = element['href']
        task = asyncio.ensure_future(scrape_link(link_url))
        tasks.append(task)

    fwd_elements = await asyncio.gather(*tasks)

    dic = {}
    for i, element in enumerate(series_elements):
        dic[element.text] = fwd_elements[i]

    sorted_dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))

    with open("comic-data.txt", "w") as f:
        for key, value in sorted_dic.items():
            f.write(f"{key}: {value}\n")

if __name__ == '__main__':
    asyncio.run(main())

# Short Description - List of all mangas available on asurascans website in descending order by how many people bookarked it 
# Story - I created this script on 24th March, 2023 because I wanted to read new manga and wanted to see which one had huge fan following.