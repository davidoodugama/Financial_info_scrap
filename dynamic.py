import requests
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

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
        time.sleep(5)
    except:
        pass
    
    return driver.page_source

driver                    = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
url                       = 'https://www.investing.com/commodities/real-time-futures'
driver.get(url)
page_source_price         = driver.page_source
loadMoreButtons           = driver.find_elements(By.CSS_SELECTOR, ".mobileAndTablet\\:overflow-x-auto.overflow-y-scroll .inv-tab")

page_source_performance   = clickButton(loadMoreButtons[1], driver)
page_source_technical     = clickButton(loadMoreButtons[2], driver)
page_source_specification = clickButton(loadMoreButtons[3], driver)

driver.close()
soup_price                = BeautifulSoup(page_source_price, 'lxml')

print(" ---------------------------------------------------------------- Real Time Commodity Futures Prices ---------------------------------------------------------------- ")
table_rows                = soup_price.find('div', class_= 'relative dynamic-table-v2_dynamic-table-wrapper__fBEvo').find('table').tbody.find_all('tr')
for row in table_rows:
    tds                   = row.find_all('td')
    name                  = tds[1].find('span', class_= 'block text-ellipsis overflow-hidden whitespace-nowrap').text
    month                 = tds[2].text
    last                  = tds[3].text
    high                  = tds[4].text.strip().replace(',', '')
    low                   = tds[5].text.strip().replace(',', '')
    change                = tds[6].text.strip().replace(',', '')
    change_percentage     = tds[7].text.strip().replace(',', '')
    time_                 = tds[8].find('time').text
    print(f"""
    Stock Name        : {name}
    Month             : {month}
    Last Value        : {last}
    High Value        : {high}
    Low Value         : {low}
    Change            : {change}
    Change Percentage : {change_percentage}
    Time              : {time_}
    """)

soup_performance          = BeautifulSoup(page_source_performance, 'lxml')

print(" ---------------------------------------------------------------- Real Time Commodity Futures Performance ---------------------------------------------------------------- ")
table_rows                = soup_performance.find('div', class_= 'relative dynamic-table-v2_dynamic-table-wrapper__fBEvo').find('table').tbody.find_all('tr')
for row in table_rows:
    tds = row.find_all('td')
    name                  = tds[1].find('span', class_= 'block text-ellipsis overflow-hidden whitespace-nowrap').text
    daily                 = tds[2].text.strip().replace(',', '')
    week_1                = tds[3].text.strip().replace(',', '')
    month_1               = tds[4].text.strip().replace(',', '')
    ytd                   = tds[5].text.strip().replace(',', '')
    year_1                = tds[6].text.strip().replace(',', '')
    year_3                = tds[7].text.strip().replace(',', '')
    print(f"""
    Stock Name        : {name}
    Daily             : {daily}
    1 Week Value      : {week_1}
    1 Month Value     : {month_1}
    YTD               : {ytd}
    1 Year Value      : {year_1}
    3 Years Value     : {year_3}
    """)

soup_technical            = BeautifulSoup(page_source_technical, 'lxml')

print(" ---------------------------------------------------------------- Real Time Commodity Futures Techincal ---------------------------------------------------------------- ")
table_rows                = soup_technical.find('div', class_= 'relative dynamic-table-v2_dynamic-table-wrapper__fBEvo').find('table').tbody.find_all('tr')
for row in table_rows:
    tds = row.find_all('td')
    name                  = tds[1].find('span', class_= 'block text-ellipsis overflow-hidden whitespace-nowrap').text
    hourly                = tds[2].text.strip().replace(',', '')
    daily                 = tds[3].text.strip().replace(',', '')
    weekly                = tds[4].text.strip().replace(',', '')
    monthly               = tds[5].text.strip().replace(',', '')
    print(f"""
    Stock Name        : {name}
    Hourly            : {hourly}
    Daily             : {daily}
    Weekly            : {weekly}
    Monthly           : {monthly}
    """)

soup_specification        = BeautifulSoup(page_source_specification, 'lxml')

print(" ---------------------------------------------------------------- Real Time Commodity Futures Specification ---------------------------------------------------------------- ")
table_rows                = soup_specification.find('div', class_= 'relative dynamic-table-v2_dynamic-table-wrapper__fBEvo').find('table').tbody.find_all('tr')
for row in table_rows:
    tds = row.find_all('td')
    name                  = tds[1].find('span', class_= 'block text-ellipsis overflow-hidden whitespace-nowrap').text
    symbol                = tds[2].text.strip().replace(',', '')
    exchange              = tds[3].text.strip().replace(',', '')
    contract_size         = tds[4].text.strip().replace(',', '')
    months                = tds[5].text.strip().replace(',', '')
    point_value           = tds[6].text.strip().replace(',', '')
    print(f"""
    Stock Name        : {name}
    Symbol            : {symbol}
    Exchange          : {exchange}
    Contract Size     : {contract_size}
    Months            : {months}
    Point Value       : {point_value}
    """)

soup                      = BeautifulSoup(page_source_price, 'lxml')

print(" ---------------------------------------------------------------- Market Movers Most Active ---------------------------------------------------------------- ")
table_rows                = soup.find('div', class_= 'pt-5 md:pt-10 xl:container xl:mx-auto font-sans-v2 antialiased text-[#232526] grid grid-cols-1 md:grid-cols-[1fr_72px] lg:grid-cols-[1fr_420px] px-4 sm:px-6 md:px-7 md:gap-6 lg:px-8 lg:gap-8 flex-1').find('div', class_= 'relative flex flex-col').find('div', class_= 'my-10', attrs={'data-test': 'market-movers'}).tbody.find_all('tr')
for row in table_rows:
    tds                   = row.find_all('td')
    name                  = tds[0].find('a').text
    last                  = tds[1].text.strip().replace(',', '')
    change_percentage     = tds[2].text.strip().replace(',', '')
    volume                = tds[3].text.strip().replace(',', '')
    print(f"""
    Market Name       : {name}
    Last Value        : {last}
    Change Percentage : {change_percentage}
    Volume            : {volume}
    """)

soup                     = BeautifulSoup(page_source_price, 'lxml')

print(" ---------------------------------------------------------------- Market Movers Gainers ---------------------------------------------------------------- ")
table_rows               = soup.find('div', class_= 'pt-5 md:pt-10 xl:container xl:mx-auto font-sans-v2 antialiased text-[#232526] grid grid-cols-1 md:grid-cols-[1fr_72px] lg:grid-cols-[1fr_420px] px-4 sm:px-6 md:px-7 md:gap-6 lg:px-8 lg:gap-8 flex-1').find('div', class_= 'relative flex flex-col').find('div', class_= 'my-10', attrs={'data-test': 'market-movers'}).find_all('table', class_= 'w-full text-xs leading-4 hidden')[0].tbody.find_all('tr')
for row in table_rows:
    tds                  = row.find_all('td')
    name                 = tds[0].find('a').text
    last                 = tds[1].text.strip().replace(',', '')
    change_percentage    = tds[2].text.strip().replace(',', '')
    volume               = tds[3].text.strip().replace(',', '')
    print(f"""
    Market Name       : {name}
    Last Value        : {last}
    Change Percentage : {change_percentage}
    Volume            : {volume}
    """)

soup                     = BeautifulSoup(page_source_price, 'lxml')

print(" ---------------------------------------------------------------- Market Movers Losers ---------------------------------------------------------------- ")
table_rows               = soup.find('div', class_= 'pt-5 md:pt-10 xl:container xl:mx-auto font-sans-v2 antialiased text-[#232526] grid grid-cols-1 md:grid-cols-[1fr_72px] lg:grid-cols-[1fr_420px] px-4 sm:px-6 md:px-7 md:gap-6 lg:px-8 lg:gap-8 flex-1').find('div', class_= 'relative flex flex-col').find('div', class_= 'my-10', attrs={'data-test': 'market-movers'}).find_all('table', class_= 'w-full text-xs leading-4 hidden')[1].tbody.find_all('tr')
for row in table_rows:
    tds                  = row.find_all('td')
    name                 = tds[0].find('a').text
    last                 = tds[1].text.strip().replace(',', '')
    change_percentage    = tds[2].text.strip().replace(',', '')
    volume               = tds[3].text.strip().replace(',', '')
    print(f"""
    Market Name       : {name}
    Last Value        : {last}
    Change Percentage : {change_percentage}
    Volume            : {volume}
    """)