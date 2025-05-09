import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
import pandas as pd

class DoctorSpider:
    def __init__(self):
        self._data = []
    
    async def crawl_page(self, page_num):
        browser = await launch(
            headless=True,
            executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe'
        )
        page = await browser.newPage()
        url = f"https://www.guahao.com/expert/all/全国/all/不限/p{page_num}"
        await page.goto(url)
        content = await page.content()
        self.parse_html(content)
        await browser.close()
    
    def parse_html(self, html):
        doc = pq(html)
        for item in doc(".g-doctor-item").items():
            name_level = item.find(".g-doc-baseinfo>dl>dt").text().split()
            data = {
                "name": name_level[0],
                "level": name_level[1],
                "department": item.find(".g-doc-baseinfo>dl>dd>p:eq(0)").text(),
                "hospital": item.find(".g-doc-baseinfo>dl>dd>p:eq(1)").text(),
                "rating": item.find(".star-count em").text(),
                "consultations": item.find(".star-count i").text()
            }
            self._data.append(data)
        
        df = pd.DataFrame(self._data)
        df.to_csv("doctors_data.csv", encoding='utf-8-sig')

if __name__ == "__main__":
    spider = DoctorSpider()
    asyncio.get_event_loop().run_until_complete(spider.crawl_page(1))