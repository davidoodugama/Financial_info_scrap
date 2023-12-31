import requests
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import WebDriverException
from urllib.parse import unquote

from selenium.webdriver.common.by import By

# session = HTMLSession()
options               = Options()
options.add_argument('start-maximized')
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)

def clickButton(loadMoreButtons, driver):
    try:
        time.sleep(2)
        loadMoreButtons.click()

        # Wait for the page to load after the click
        WebDriverWait(driver, 15).until(
            EC.staleness_of(loadMoreButtons)
        )
    except Exception as e:
        print(f"Error clicking button: {e}")
    
    return driver.page_source

def extract_table_info(table_rows, headers, type):
    if type == 'export':
        for rows in table_rows:
            tds                                  = rows.find_all('td')
            code                                 = tds[1].text.strip().replace(',', '')
            product_label                        = tds[2].text.strip().replace(',', '')
            export_value                         = tds[3].text.strip().replace(',', '')
            trade_balance                        = tds[4].text.strip().replace(',', '')
            annual_growth_1                      = tds[5].text.strip().replace(',', '')
            annual_growth_2                      = tds[6].text.strip().replace(',', '')
            annual_growth_of_world               = tds[7].text.strip().replace(',', '')
            share_in_world                       = tds[8].text.strip().replace(',', '')
            ranking_in_world                     = tds[9].text.strip().replace(',', '')
            average_distance_of_supply_countries = tds[10].text.strip().replace(',', '')
            concentration_of_supplying_countries = tds[11].text.strip().replace(',', '')
            
            print(f"""
            Code: {code}
            Product Label: {product_label}
            {headers[0]}: {export_value}
            {headers[1]}: {trade_balance}
            {headers[2]}: {annual_growth_1}
            {headers[3]}: {annual_growth_2}
            {headers[4]}: {annual_growth_of_world}
            {headers[5]}: {share_in_world}
            {headers[6]}: {ranking_in_world}
            {headers[7]}: {average_distance_of_supply_countries}
            {headers[8]}: {concentration_of_supplying_countries}
            """)
    
driver_path = ChromeDriverManager().install()
soups = []
# /root/.wdm/drivers/chromedriver/linux64/120.0.6099.109/chromedriver-linux64/chromedriver
chrome_service = Service(executable_path=str(driver_path))

driver              = webdriver.Chrome(service=chrome_service, options= options)
url                 = 'https://www.trademap.org/Product_SelProductCountry.aspx?nvpm=1%7c144%7c%7c%7c%7cTOTAL%7c%7c%7c2%7c1%7c1%7c2%7c1%7c%7c1%7c1%7c1%7c1'
decoded_url         = unquote(url)

try:
    driver.get(decoded_url)
    driver.implicitly_wait(10)
except:
    driver.close()
    driver = webdriver.Chrome(service=chrome_service, options= options)
    
    driver.get(decoded_url)
    while driver.page_source == None:
        driver.get(decoded_url)
        driver.implicitly_wait(10)

page_source  = driver.page_source
pages        = []

def getElement():
    div_container = driver.find_element(By.ID, 'div_container')
    tables        = div_container.find_elements(By.TAG_NAME,'table')
    target_table  = tables[-4]
    tbody         = target_table.find_element(By.TAG_NAME,'tbody')
    tr            = tbody.find_element(By.XPATH,'//tr[@align="right" and @style="color:White;background-color:#86B3E0;font-size:80%;"]')
    td_table      = tr.find_element(By.TAG_NAME,'td').find_element(By.TAG_NAME,'table')
    td_tbody      = td_table.find_element(By.TAG_NAME,'tbody')
    td_tr         = td_tbody.find_element(By.TAG_NAME,'tr')
    
    return td_tr

td_tr = getElement()
tds   = td_tr.find_elements(By.TAG_NAME,'td')[1:]
id    = 1
for td in tds:
    try:
        td.get_attribute("innerHTML")
        pages.append(BeautifulSoup(clickButton(td, driver), 'lxml'))
        id += 1
    except:
        td_tr = getElement()
        td_1 = td_tr.find_elements(By.TAG_NAME,'td')[id]
        pages.append(BeautifulSoup(clickButton(td_1, driver), 'lxml'))
        id += 1

driver.close()
soup       = BeautifulSoup(page_source, 'lxml')
table_rows = soup.find('div', attrs= {'id' :'div_container'}).find_all('table')[-4].tbody.find_all('tr', attrs= {"style": "color:White;background-color:#5D7B9D;font-size:80%;font-weight:bold;"})[1].find_all('th')
headers = []
for header in table_rows:
    headers.append(header.a.text)

# EXTRACT FIRST PAGE
table_rows = soup.find('div', attrs= {'id' :'div_container'}).find_all('table')[-4].tbody.find_all('tr', attrs= {"align": "right"})[2:-1]
extract_table_info(table_rows, headers, 'export')

# EXTRACT REST OF THE PAGES
for page in pages:
    table_rows = page.find('div', attrs= {'id' :'div_container'}).find_all('table')[-4].tbody.find_all('tr', attrs= {"align": "right"})[2:-1]
    extract_table_info(table_rows, headers, 'export')