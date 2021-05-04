import asyncio
import aiohttp
from lxml import html
from random import choice


with open('keys.txt', 'r') as f:
    keys = [line.strip() for line in f if line]

with open('agents.txt', 'r') as f:
    agents = [line.strip() for line in f if line]


async def crawler(keyword,  sem, agents):
    async with sem:
        url = f'https://www.google.com/search?q={keyword}'
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 '
            #               'Safari/537.36'
            'User-Agent': f'{choice(agents)}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                print(response.status, url)
                html_code = await response.text()
            dom_tree = html.fromstring(html_code)
            links = dom_tree.xpath('//dive[@class="r"]/a[1]/@href')
            print(links)
            with open('results.txt', 'a') as f:
                for link in links:
                    f.write(f'{keyword}\t{link}\n')


async def main():
    tasks = []
    sem = asyncio.Semaphore(20)
    print('!!!!!')

    for key in keys:
        print(key)
        task = asyncio.Task(crawler(key, sem, agents))
        tasks.append(task)


loop = asyncio.get_event_loop()

loop.run_until_complete(main())
