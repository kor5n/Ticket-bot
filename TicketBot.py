from dotenv import load_dotenv
import os
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path="/Users/kor5n/Desktop/chromedriver")
driver.get("https://www.tottenhamhotspur.com/tickets/buy-tickets/home-tickets/")



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
        if message.content.startswith("/Find Spurs tickets"):
            channel = message.channel
            await channel.send("YES SIR!")
            await self.monitoring_spurs(message)    
    async def monitoring_spurs(self, message):
        findingTickets = True
        while findingTickets == True:
            sleep(10)
            try:
                driver.find_element(By.XPATH, "//div[text() = '25 Oct']")#Type the date when tickets will be out              
            except:            
                driver.save_screenshot('screenshot.png')
                channel = message.channel
                scroll_down = "window.scrollBy(0,1000);"
                driver.execute_script(scroll_down)
                await channel.send(file=discord.File('screenshot.png'))
                findingTickets = False
        driver.quit()       
        
            

intents = discord.Intents.default()
intents.members = True

client = CustomClient(intents=intents)
client.run(TOKEN)