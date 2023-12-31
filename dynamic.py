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
options = Options()
options.add_argument('start-maximized')
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)

driver_path    = ChromeDriverManager().install()
chrome_service = Service(executable_path=str(driver_path))

driver         = webdriver.Chrome(service=chrome_service, options= options)
url            = 'https://tradingeconomics.com/'
matrix_url     = 'https://tradingeconomics.com/matrix'
crypto_url     = 'https://tradingeconomics.com/crypto'

driver.get(url)
driver.implicitly_wait(10)

page_source  = driver.page_source

driver.get(matrix_url)
driver.implicitly_wait(10)

page_source_matrix  = driver.page_source

driver.get(crypto_url)
driver.implicitly_wait(10)

page_source_crypto  = driver.page_source
driver.close()

soup         = BeautifulSoup(page_source, 'lxml')
soup_matrix  = BeautifulSoup(page_source_matrix, 'lxml')
soup_crypto  = BeautifulSoup(page_source_crypto, 'lxml')

# CARD INFORMATION
print("")
print(" ----------------------------------------------------------- CARD INFO ----------------------------------------------------------- ")
cards = soup.find('div', class_= 'row', attrs={"id":"hometiles"}).find_all('div', class_= 'col-lg-4 col-md-6 col-xs-12')
for card in cards:
    heading      = card.find('div', class_= 'home-tile-inside').b.text.strip()
    divs         = card.find('div', class_= 'home-tile-inside').find_all('div')
    message      = divs[0].text.strip().strip()
    updated_time = divs[1].text.strip().strip()
    print(f"""
    Heading     : {heading}
    Message     : {message}
    Updated Time: {updated_time}
    """)

# CALENDAR INFORMATION
print("")
print(" ----------------------------------------------------------- CALENDAR INFO ----------------------------------------------------------- ")
calendar_data_rows = soup.find('div', class_= 'calendar-widget thumbnail').find_all('div', class_= 'calendar-widget-event')
for row in calendar_data_rows:
    time_   = ''.join(row.find('span', class_= 'calendar-widget-time').find_all(string=True, recursive=False)).strip()
    message = ' '.join(row.a.span.text.strip().split())
    print(f"""
    Time    : {time_}
    Message : {message}
    """)

# GDP INFORMATION
print("")
print(" ----------------------------------------------------------- GDP INFO ----------------------------------------------------------- ")
gdp_info_table_rows = soup_matrix.find('div', class_= 'card').find('table', class_= 'table table-hover sortable-theme-minimal table-heatmap').tbody.find_all('tr')
for row in gdp_info_table_rows:
    tds             = row.find_all('td')
    country         = tds[0].text.strip()
    gdp             = tds[1].text.strip()
    gdp_growth      = tds[2].text.strip()
    interst_rate    = tds[3].text.strip()
    inflation_rate  = tds[4].text.strip()
    jobless_rate    = tds[5].text.strip()
    gov_budget      = tds[6].text.strip()
    debt_gdp        = tds[7].text.strip()
    current_account = tds[8].text.strip()
    population      = tds[9].text.strip()
    
    print(f"""
    Country           : {country}
    GDP               : {gdp}
    GDP Growth        : {gdp_growth}
    Interst Rate      : {interst_rate}
    Inflation Rate    : {inflation_rate}
    Jobless Rate      : {jobless_rate}
    Government Budget : {gov_budget}
    Debt/GDP          : {debt_gdp}
    Current Account   : {current_account}
    Population        : {population}
    """)
    
div_cards = soup_crypto.find('div', class_= 'col-xl-12').find_all('div', class_= 'card')

# CRYPTO
print("")
print(" ----------------------------------------------------------- CRYPTO ----------------------------------------------------------- ")
crypto_info_table_rows = div_cards[0].find('table', class_= 'table table-hover table-striped table-heatmap').tbody.find_all('tr')
for row in crypto_info_table_rows:
    tds               = row.find_all('td')
    crypto            = tds[0].text.strip()
    price             = tds[1].text.strip()
    day               = tds[2].text.strip()
    day_change_status = tds[2].span.get('class')[0].split('-')[1]
    percentage        = tds[3].text.strip()
    weekly            = tds[4].text.strip()
    monthly           = tds[5].text.strip()
    yoy               = tds[6].text.strip()
    market_cap        = tds[7].text.strip()
    date              = tds[8].text.strip()
    
    print(f"""
    Crypto            : {crypto}
    Price             : {price}
    Day               : {day}
    Day Change Status : {day_change_status}
    Percentage        : {percentage}
    Weekly            : {weekly}
    Monthly           : {monthly}
    YoY               : {yoy}
    Market Cap        : {market_cap}
    Date              : {date}
    """)

# BTC
print("")
print(" ----------------------------------------------------------- BTC ----------------------------------------------------------- ")
btc_info_table_rows   = div_cards[1].find('table', class_= 'table table-hover table-striped table-heatmap').tbody.find_all('tr')
for row in btc_info_table_rows:
    tds               = row.find_all('td')
    btc               = tds[0].text.strip()
    price             = tds[1].text.strip()
    day               = tds[2].text.strip()
    day_change_status = tds[2].span.get('class')[0].split('-')[1]
    percentage        = tds[3].text.strip()
    weekly            = tds[4].text.strip()
    monthly           = tds[5].text.strip()
    yoy               = tds[6].text.strip()
    date              = tds[7].text.strip()
    
    print(f"""
    BTC               : {btc}
    Price             : {price}
    Day               : {day}
    Day Change Status : {day_change_status}
    Percentage        : {percentage}
    Weekly            : {weekly}
    Monthly           : {monthly}
    YoY               : {yoy}
    Date              : {date}
    """)

# ETH
print("")
print(" ----------------------------------------------------------- ETH ----------------------------------------------------------- ")
eth_info_table_rows   = div_cards[2].find('table', class_= 'table table-hover table-striped table-heatmap').tbody.find_all('tr')
for row in eth_info_table_rows:
    tds               = row.find_all('td')
    eth               = tds[0].text.strip()
    price             = tds[1].text.strip()
    day               = tds[2].text.strip()
    day_change_status = tds[2].span.get('class')[0].split('-')[1]
    percentage        = tds[3].text.strip()
    weekly            = tds[4].text.strip()
    monthly           = tds[5].text.strip()
    yoy               = tds[6].text.strip()
    date              = tds[7].text.strip()
    
    print(f"""
    ETH               : {eth}
    Price             : {price}
    Day               : {day}
    Day Change Status : {day_change_status}
    Percentage        : {percentage}
    Weekly            : {weekly}
    Monthly           : {monthly}
    YoY               : {yoy}
    Date              : {date}
    """)