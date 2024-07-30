from dotenv import load_dotenv
import os
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

#dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PATH = os.getenv("CHROMEDRIVER")

#discord intents
intents = discord.Intents()
intents.members = True

#url
url_path = ""

class CustomClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    async def on_message(self, message):
        if message.content.startswith("/Find Spurs tickets"):
            channel = message.channel
            #await self.find_path(message)
            await channel.send("YES SIR!")
            await self.monitoring_spurs(message)
        if message.content.startswith("/Find DIF tickets"):
            channel = message.channel
            await self.find_path(message)
            await channel.send("YES SIR!")
            await self.monitoring_dif(message)   
    async def monitoring_dif(self, message):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(options=options, executable_path=PATH)
        try:
            driver.get(url_path)
        except:
            self.failed_url()

        finding_tickets = True
        while finding_tickets == True:
            sleep(125)
            driver.refresh()
            try:
                element = driver.find_element(By.XPATH, "/html/body/article/div/header/div[4]/div/button/a")
                driver.save_screenshot('screenshot.png')
                channel = message.channel
                await channel.send("@everyone\nDIF tickets are out!")
                await channel.send(file=discord.File('screenshot.png'))
                element.click()
                await channel.send("@everyone\nDIF tickets are out!")
                await channel.send(file=discord.File('screenshot.png'))
                finding_tickets = False
            except:
                print("we didnt find tickets")
        driver.quit()
    async def monitoring_spurs(self, message):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(options=options, executable_path=PATH)
        driver.get("https://www.tottenhamhotspur.com/tickets/buy-tickets/home-tickets/?utm_source=thfc&utm_medium=quicklink&utm_campaign=alwayson")


        findingTickets = True
        while findingTickets == True:
            sleep(125)
            driver.refresh()
            try:
                driver.find_element(By.XPATH, "//div[text() = '"+url_path[:2]+ " "+url_path[2:]+"]")#Type the date when tickets will be out
                print("we didnt find tickets")            
            except:            
                
                channel = message.channel
                driver.execute_script("window.scrollBy(0,1000);")
                href = element.get_attribute("href")
                print("we found tickets")
                print(href)
                driver.get(href)
                driver.save_screenshot("screenshot.png")
                await channel.send(file=discord.File('screenshot.png'))
                await channel.send("@everyone!\nSpurs tickets are out!")
                findingTickets = False
        driver.quit()  
    async def find_path(self, message):
        global url_path
        result = message.content.split()
        url_path = result[3]
    async def failed_url(self,message):
        channel = message.chanel
        await channel.send("failed to read url")

intents = discord.Intents.default()
intents.members = True

client = CustomClient(intents=intents)
client.run(TOKEN)
