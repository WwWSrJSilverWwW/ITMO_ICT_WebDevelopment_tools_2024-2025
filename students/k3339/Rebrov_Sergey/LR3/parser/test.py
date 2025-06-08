import asyncio
import aiohttp

async def fetch_html(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html

if __name__ == "__main__":
    url = "https://codenrock.com/contests/kubok-rossii-po-sportivnomu-programmirov/"
    html = asyncio.run(fetch_html(url))
    print(html)  # выводит HTML-код страницы
