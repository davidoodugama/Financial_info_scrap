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
options = Options()
options.add_argument('start-maximized')
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
# daily = driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
# daily = driver
url = 'https://www.ceicdata.com/en/sri-lanka/transportation/lk-logistics-performance-index-1low-to-5high-ease-of-arranging-competitively-priced-shipments'

driver.get(url)
loadMoreButtons = driver.find_elements(By.CLASS_NAME, 'load-more')

try:
    for loadMoreButton in loadMoreButtons:
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(5)
except:
    pass
page_source = driver.page_source
driver.close()

soup = BeautifulSoup(page_source, 'lxml')

information_of_sl_container_throughput = soup.find('p', class_= 'mxw-88 mt-38')

print('')
print(' --------------------------------------------------------------- Related Indicators for Sri Lanka LK: Logistics Performance Index: 1=Low To 5=High: Ease of Arranging Competitively Priced Shipments --------------------------------------------------------------- ')
throuput_table = soup.find('table', class_= 'dp-table dp-table-auto').tbody.find('tr').find_all('td')
last_throughput_amount = throuput_table[0].find_all('span')[0].text.strip().replace(',', '')
last_throughput_year = throuput_table[0].find_all('span')[2].text

previous_throughput_amount = throuput_table[1].find_all('span')[0].text.strip().replace(',', '')
previous_throughput_year = throuput_table[1].find_all('span')[2].text

min_throughput_amount = throuput_table[2].contents[0].strip().replace(',', '')
min_throughput_year = throuput_table[2].span.text

max_throughput_amount = throuput_table[3].contents[0].strip().replace(',', '')
max_throughput_year = throuput_table[3].span.text

unit = throuput_table[4].text.strip().replace(',', '')
frequency = throuput_table[5].text.strip().replace(',', '')
range = throuput_table[6].text.strip().replace(',', '')

print(f"""
Last: {last_throughput_amount}
Last Year: {last_throughput_year}
Previous: {previous_throughput_amount}
Previous Year: {previous_throughput_year}
Min: {min_throughput_amount}
Min Year: {min_throughput_year}
Max: {max_throughput_amount}
Max Year: {max_throughput_year}
Unit: {unit}
Frequency: {frequency}
Range: {range}     
""")
print('')
print(' --------------------------------------------------------------- RELATED INDICATORS --------------------------------------------------------------- ')
tb_rows = soup.find('div', attrs= {'id': 'op-table-related'}).find('table', class_= 'dp-table').tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    related_indicator = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    container_port_throughput_frequency = get_row_info[2].text.strip()
    container_port_throughput_range = get_row_info[3].text.strip()
    print(f"""
    Related Indicator: {related_indicator}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {container_port_throughput_frequency}
    Range: {container_port_throughput_range}
    """)
print('')
print(' --------------------------------------------------------------- SL Key Series --------------------------------------------------------------- ')
tables = soup.find('div', attrs= {'id': 'op-table-categories'}).find_all('table', class_= 'dp-table')
tb_rows = tables[0].tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    national_account = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    frequency = get_row_info[2].text.strip()
    range = get_row_info[3].text.strip()
    print(f"""
    National Accounts: {national_account}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {frequency}
    Range: {range}
    """)

print('')
print(' --------------------------------------------------------------- PRODUCTION  --------------------------------------------------------------- ')
tables = soup.find('div', attrs= {'id': 'op-table-categories'}).find_all('table', class_= 'dp-table')
tb_rows = tables[1].tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    production = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    frequency = get_row_info[2].text.strip()
    range = get_row_info[3].text.strip()
    print(f"""
    Foreign Trade: {production}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {frequency}
    Range: {range}
    """)

print('')
print(' --------------------------------------------------------------- GOVERNMENT AND PUBLIC FINANCE --------------------------------------------------------------- ')
tb_rows = tables[2].tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    g_p_finance = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    frequency = get_row_info[2].text.strip()
    range = get_row_info[3].text.strip()
    print(f"""
    Balance of Payments: {g_p_finance}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {frequency}
    Range: {range}
    """)

print('')
print(' --------------------------------------------------------------- DEMOGRAPHIC AND LABOUR MARKET	 --------------------------------------------------------------- ')
tb_rows = tables[3].tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    demographic_labour_market = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    frequency = get_row_info[2].text.strip()
    range = get_row_info[3].text.strip()
    print(f"""
    Demographic And Labour Market: {demographic_labour_market}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {frequency}
    Range: {range}
    """)

print('')
print(' --------------------------------------------------------------- DEMOGRAPHIC AND LABOUR MARKET --------------------------------------------------------------- ')
tb_rows = tables[4].tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    domestic_trade_household = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    frequency = get_row_info[2].text.strip()
    range = get_row_info[3].text.strip()
    print(f"""
    Domestic Trade And Household Survey: {domestic_trade_household}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {frequency}
    Range: {range}
    """)

print('')
print(' --------------------------------------------------------------- MORE INDICATORS FOR SRI LANKA --------------------------------------------------------------- ')
tb_rows = soup.find('div', attrs= {'id': 'left-col-7'}).find_all('div', attrs= {'id': 'op-table-related'})[-1].find('table', class_= 'dp-table').tbody.find_all('tr')
for row in tb_rows:
    get_row_info = row.find_all('td')
    indicator = get_row_info[0].a.text.strip()
    last_color = get_row_info[1].find_all('span')[0].get('class')
    last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
    color_name = last_amount_status.group(1) if last_amount_status else None
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
    last_year = get_row_info[1].find_all('span')[2].text.strip()
    frequency = get_row_info[2].text.strip()
    range = get_row_info[3].text.strip()
    print(f"""
    indicator: {indicator}
    Last Amount: {last_amount}
    Change_Status: {change_status}
    Last Amount Year: {last_year}
    Frequency: {frequency}
    Range: {range}
    """)