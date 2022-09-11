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

class CustomClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    async def on_message(self, message):
        if message.content.startswith("/Find Spurs tickets"):
            channel = message.channel
            await channel.send("YES SIR!")
            await self.monitoring_spurs(message)
        if message.content.startswith("/Find DIF tickets"):
            channel = message.channel
            await channel.send("YES SIR!")
            await self.monitoring_dif(message)   
    async def monitoring_dif(self, message):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(options=options, executable_path=PATH)
        driver.get("https://dif.se/kalender/2020-2029/2022/matcher/herrar/allsvenskan/hammarby-djurgarden")

        finding_tickets = True
        while finding_tickets == True:
            sleep(125)
            try:
                element = driver.find_element(By.XPATH, '//*[@id="ModuleCalendarInformation"]/div/div[1]/div[2]/ul/li/div/div/a')
                driver.save_screenshot('screenshot.png')
                channel = message.channel
                await channel.send("@everyone\nDIF tickets are out!")
                await channel.send(file=discord.File('screenshot.png'))
                finding_tickets = False
                element.click()
            except:
                print("we didnt find tickets")
        driver.quit()
    async def monitoring_spurs(self, message):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Chrome(options=options, executable_path=PATH)
        driver.get("https://www.tottenhamhotspur.com/tickets/buy-tickets/home-tickets/")

        findingTickets = True
        while findingTickets == True:
            sleep(125)
            try:
                driver.find_element(By.XPATH, "//div[text() = '27 Sep']")#Type the date when tickets will be out
                print("we didnt find tickets")            
            except:            
                
                channel = message.channel
                driver.execute_script("window.scrollBy(0,1000);")
                driver.save_screenshot('screenshot.png')
                await channel.send(file=discord.File('screenshot.png'))
                await channel.send("@everyone!\nSpurs tickets are out!")
                print("we found tickets")
                findingTickets = False
        driver.quit() 
        
            

intents = discord.Intents.default()
intents.members = True

client = CustomClient(intents=intents)
client.run(TOKEN)