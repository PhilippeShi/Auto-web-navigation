from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import os
import threading



def create_driver():
    """
    Create an instance of web driver
    File must be in the same directory

    :return: webdriver
    """
    current_file_path = Path(__file__).absolute()
    parent_path = Path(current_file_path.absolute().parent.absolute())
    chrome_driver_name = "chromedriver.exe"
    chromedriver_PATH = os.path.join(parent_path, chrome_driver_name)
    driver = webdriver.Chrome(chromedriver_PATH)
    driver.maximize_window()
    return driver


def new_website(url, new_tab = True):
    """
    Open an url link in a new tab of the current instance of web driver
    If it is the first tab is empty, use it instead
    :param url: string
    :param new_tab: boolean create new tab or not, default = True
    """
    if (new_tab == True) and driver.current_url != "data:,":
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

    driver.get(url)


def search_google(topic, new_tab = True):
    new_website("https://www.google.ca", new_tab)

    inpt = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    inpt.send_keys(topic)
    inpt.send_keys(Keys.RETURN)


def get_sections(new_tab = True):
    new_website("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin", new_tab)

    pw_PATH = os.path.join(parent_path, "password.txt")
    pw = open(pw_PATH, "r")


    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mcg_un")))
    username.click()
    username.send_keys("philippe.shi@mail.mcgill.ca")

    password = driver.find_element_by_id("mcg_pw")
    password.click()
    password.send_keys(pw.read())
    pw.close()

    driver.find_element_by_id("mcg_un_submit").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "keyword_in_id")))

    driver.get("https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search")

    # Getting the term
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "p_term")))
    select_term = Select(driver.find_element_by_name("p_term"))
    select_term.select_by_visible_text("Fall 2021")
    driver.find_element_by_xpath("/html/body/div[3]/form/input[3]").click()

    # Getting the subject (major)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "sel_subj")))
    select_term = Select(driver.find_element_by_xpath("""//*[@id="subj_id"]"""))
    select_term.select_by_visible_text("ECSE - Electrical Engineering")
    driver.find_element_by_xpath("/html/body/div[3]/form/input[17]").click()

    # Viewing sections for 324
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/table[2]/tbody/tr[17]/td[3]/form/input[30]")))
    driver.find_element_by_xpath("/html/body/div[3]/table[2]/tbody/tr[16]/td[3]/form/input[30]").click()

    tutorial_7_name = driver.find_element_by_xpath("/html/body/div[3]/form/table/tbody/tr[21]/td[5]").text+ ": "
    tutorial_7_seats = driver.find_element_by_xpath("/html/body/div[3]/form/table/tbody/tr[21]/td[13]").text
    tutorial_7 = tutorial_7_name + tutorial_7_seats + "\n"

    lab_9_name = driver.find_element_by_xpath("/html/body/div[3]/form/table/tbody/tr[27]/td[5]").text + ": "
    lab_9_seats = driver.find_element_by_xpath("/html/body/div[3]/form/table/tbody/tr[27]/td[14]").text
    lab_9 = lab_9_name + lab_9_seats + "\n"

    f.write("=================\n")
    f.write(tutorial_7)
    f.write(lab_9)


    if open_screenshots:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.save_screenshot("sections.png")
        os.startfile("sections.png")


def velo_newgear(new_tab = True):
    new_website("https://www.velonewgear.com/en/product/bikes-shops/", new_tab)

    select_color = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "couleurs-cadre")))
    select_color.click()


    colors_list = select_color.text.split("\n")

    name = driver.find_element_by_xpath("""//*[@id="product-37511"]/div[2]/h1""")

    f.write("=================\n" + name.text + "\n")
    for i in colors_list:
        if i != "Choose an option":
            f.write(i + "\n")

    if open_screenshots:
        driver.save_screenshot("frame_colors.png")
        os.startfile("frame_colors.png")



""" Main run """
open_screenshots = input("Open screenshots? (smth = yes, nothing = no) \nEnter: ")
if len(open_screenshots) == 0:
    open_screenshots = False
else:
    open_screenshots = True
current_file_path = Path(__file__).absolute()
parent_path = Path(current_file_path.absolute().parent.absolute())
text_file_path = os.path.join(parent_path, "results.txt")

f = open(text_file_path, "w")

driver = create_driver()

# threading.Thread(target=velo_newgear()).start()
# threading.Thread(target=get_sections()).start()
# threading.Thread(target=search_google("reddit" )).start()

# velo_newgear()
get_sections()

f.close()
os.startfile(text_file_path)
driver.quit()

if open_screenshots:
    os.remove("frame_colors.png")
    os.remove("sections.png")

os.remove(text_file_path)

