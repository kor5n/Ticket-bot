import asyncio
from pyppeteer import launch
import random

class FootParser():
    def __init__(self):
        self.dict = {"Opponent":[],"OneHotspur":[], "OneHotspur+": []}
        self.browser = None
        self.page = None
    async def parse_spurs(self):
        await self.access_url("https://www.tottenhamhotspur.com/tickets/buy-tickets/home-tickets/")
        divs = await self.page.querySelectorAll(".TicketAvailabilityTier__cta")
        
        text = await self.page.querySelectorAll(".text--highlight")
        await asyncio.sleep(random.uniform(2, 5))
        for topic in text:
            title = await topic.querySelector("span")
            t = await title.getProperty("innerHTML")
            self.dict["Opponent"].append(await t.jsonValue())
        count = 0
        await asyncio.sleep(random.uniform(2, 5))
        for div in divs:
            divChild = await div.querySelectorAll("div")
            for vid in divChild:
                
                divProp = await vid.getProperty("innerHTML")
                divPropJson = await divProp.jsonValue()
                if "Buy Now" in divPropJson:
                    divProp = await divProp.getProperty("innerHTML")
                    divPropJson = await divProp.jsonValue()
                if divPropJson == None:
                    self.dict["OneHotspur"].append("Buy now")
                    self.dict["OneHotspur+"].append("Buy now")
                elif "Enquire" not in divPropJson and "Info" not in divPropJson:
                    if count == 1 or count % 2 != 0:
                        self.dict["OneHotspur"].append(divPropJson)
                    elif count == 0 or count % 2 ==0:
                        self.dict["OneHotspur+"].append(divPropJson)
                count += 1
    async def buy_spurs(self, team, sub):
        if team in self.dict["Opponent"]:
            index = self.dict["Opponent"].index(team)
            print(self.dict[sub][index] + "\n")
            self.scroll_down(5, 10, 10)
            if "Buy now" == self.dict[sub][index]:
                divs = await self.page.querySelectorAll(".TicketAvailabilityTier__cta")
                if sub == "OneHotspur":
                    mydiv = divs[index * index + 1]
                elif sub == "OneHotspur+":
                    mydiv = divs[index * index]
                mybutton = await mydiv.querySelector("a")
                #await mybutton.click()
                myhref = await self.page.evaluate('(element) => element.href', mybutton)
                await asyncio.sleep(random.uniform(2, 5))
                await self.page.goto(myhref)
                await self.page.screenshot({'path': 'example.png'})
            else:
                print("Tickets are not out yet")
        else:
            print("This team doesnt exist")
        await asyncio.sleep(random.uniform(100, 1000))
        await self.browser.close()
    async def access_url(self, url):
        self.browser = await launch(headless=False)
        context = await self.browser.createIncognitoBrowserContext()
        self.page = await context.newPage()
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        await self.page.setViewport({'width': 1280, 'height': 800})
        await self.page.goto(url)
        await asyncio.sleep(random.uniform(2, 5))
        try:
            await self.page.click("#onetrust-accept-btn-handler")
        except Exception as e:
            print(e)
    async def scroll_down(self, min, max, times):
        for _ in range(times):
            await self.page.evaluate(f'window.scrollBy(0, {random.uniform(min, max)})')
            await asyncio.sleep(1)

parser = FootParser()
asyncio.get_event_loop().run_until_complete(parser.parse_spurs())
asyncio.get_event_loop().run_until_complete(parser.buy_spurs("Everton", "OneHotspur"))

print(parser.dict["OneHotspur"])
print("\n", parser.dict["OneHotspur+"])

#async def dif():
 #   browser = await launch()
  #  page = await browser.newPage()
   # await page.goto('https://diffotboll.ebiljett.nu/')
   # await page.screenshot({'path': 'example.png'})

    #element = await page.querySelectorAll("html")
    #inner = await page.evaluate('(element) => element.innerHTML', element)
    #print(inner)
    #await browser.close()

#asyncio.get_event_loop().run_until_complete(spurs())

