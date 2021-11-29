from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import time
import os
from pathlib import Path
user_input = input("Enter the song/playlist/artist: ")

#Setting up driver
current_file_path = Path(__file__).absolute()
parent_path = Path(current_file_path.absolute().parent.absolute())



driver_path = os.path.join(parent_path, "chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--incognito")

# # Comment/uncomment from brave_path to driver 
# brave_path = """C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"""
# options.binary_location = brave_path
# # options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

# # Comment/uncomment from 
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

driver.get("""https://accounts.spotify.com/""")

username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-username")))
username.clear()
username.send_keys("email.txt")

pw_PATH = os.path.join(parent_path, "password.txt")
pw = open(pw_PATH, "r").readline()
password = driver.find_element_by_id("login-password")
password.clear()
password.send_keys(pw)

# Removing Remember Account
rem = driver.find_element_by_id("login-remember")
if "not-empty" in rem.get_attribute("class"):
    webdriver.ActionChains(driver).click(rem).perform()

driver.find_element_by_id("login-button").click()
time.sleep(0.75)

# getting in Web Player

# x = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TEXT , )))
x = driver.find_element_by_link_text("WEB PLAYER")
x.click()
time.sleep(0.75)

# click on search
search = driver.find_element_by_link_text("Search")
search.click()
time.sleep(0.25)

# Typing the song/artist/playlist
search = driver.find_element_by_xpath("""/html/body/div[4]/div/div[2]/div[1]/header/div[3]/div/div/form/input""")
search.send_keys(user_input)
time.sleep(1.75)

# Hover over the top result then click on the green play button
element_to_hover = driver.find_element_by_xpath("""/html/body/div[4]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/div/div/div/section[1]/div[2]/div/div""")
hover = ActionChains(driver).move_to_element(element_to_hover)
hover.perform()

time.sleep(0.1)
driver.find_element_by_xpath("""/html/body/div[4]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/div/div/div/section[1]/div[2]/div/div/div/div[3]/button""").click()
