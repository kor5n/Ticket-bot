from urllib import response
from dotenv import load_dotenv
import os
import discord
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path="/Users/kor5n/Desktop/chromedriver")
driver.get("https://dif.se/kalender/2020-2029/2022/matcher/herrar/allsvenskan/djurgarden-elfsborg")
found_tickets = False



#dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


#discord intents
intents = discord.Intents()
intents.members = True

class CustomClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    async def on_message(self, message):
        if message.content.startswith("/HELLO"):
            channel = message.channel
            await channel.send("I WANT WORK!")    
    async def monitoring_dif(self, message):
        while found_tickets != True:
            try:
                waiting = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.Class, "component-cta-button component-cta-button--large"))
                    )
            finally:
                print("We found the button")
                driver.save_screenshot('screenshot.png')
                channel = message.channel
                await channel.send("@KorvenH!")
                await channel.send(file=discord.File('screenshot.png'))
                driver.quit() 
                found_tickets = True
        
            

intents = discord.Intents.default()
intents.members = True

client = CustomClient(intents=intents)
client.run(TOKEN)