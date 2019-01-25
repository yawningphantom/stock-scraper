import asyncio
import requests
import concurrent.futures
from bs4 import BeautifulSoup as soup

url_list = ["https://www.moneycontrol.com/india/stockpricequote/miscellaneous/adanigaslimited/ADG01",
            "https://www.moneycontrol.com/india/stockpricequote/finance-general/geojitfinancialservices/GBN01"]


async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_list[i]
            )
            for i in range(len(url_list))
        ]
        ls = []
        for response in await asyncio.gather(*futures):
            ls.append(response)
        
        for data in ls:
            page_soup = soup(data.text, "html.parser")
            price = page_soup.find(id="Bse_Prc_tick")
            print(price.strong.text)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())