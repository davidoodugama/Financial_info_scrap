import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.by import By
from requests_html import HTMLSession


options = Options()
options.add_argument('start-maximized')
options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
    
def x_rates():
    html_page = requests.get("https://www.x-rates.com/table/?from=LKR&amount=1").text

    soup = BeautifulSoup(html_page, 'lxml')
    # TOP 10 
    print(" ----------------------------------------------------------------- Top 10 ------------------------------------------------------------------ ")
    currencies = soup.find('table', class_= 'ratesTable').tbody
    tb_rows = currencies.find_all('tr')
    for row in tb_rows:
        country = row.td.text
        currency_code_links = row.find_all('td', class_='rtRates')
        foreign_rate = currency_code_links[0].find('a')['href'].split('to=')[1]
        sl_rate = currency_code_links[1].find('a')['href'].split('to=')[1]
        print('SL', sl_rate, currency_code_links[1].text)
        print(f"""
              {country}: Currency Type: {foreign_rate} = {currency_code_links[0].text} | SL: Currency Type: LKR = {currency_code_links[1].text}
              """)
    print('---------------------------------------------------------------------------------------------------------------------------------------------')
    
    print(" Alphabetical order ")
    currencies = soup.find('table', class_= 'tablesorter ratesTable').tbody
    curr_rows = currencies.find_all('tr')
    for row in curr_rows:
        country = row.td.text
        currency_code = row.find_all('td', class_= 'rtRates')
        curr_type = currency_code[0].find('a')['href'].split('to=')[1]
        rate_per_lkr = currency_code[0].text
        inv_lkr = currency_code[1].text
        print(f"""{country}: Currency Type: {curr_type} = {rate_per_lkr} | SL: Currency Type: LKR = {inv_lkr}
            """)

def worldbank():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
    # global driver
    url = 'https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=LK&name_desc=false'
    driver.get(url)
    time.sleep(7)
    page_source = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_source, 'lxml')
    
    # GET THE SELECTED COUNTRY GDP INFORMATION
    section_1 = soup.find('div', class_= 'infinite')
    section_div = section_1.find_all('div', class_='item')
    divs = section_div[1].find_all('div')
    selected_country = divs[0].find('a', class_= 'country-name').text#.div
    year = divs[1].text
    gdp_for_selected_country = divs[2].text

    print(f"Sri Lanka: {selected_country}| Year: {year}| GDP: {gdp_for_selected_country}") 
    print('---------------------------------------------------------------------------------------------------------------------------------------------')
    # GET ALL GDP RELATED INFORMATION IN EVERY COUNTRY
    section_2 = soup.find('div', class_= 'infinite', attrs={"data-reactid":"432"})
    country_details_list = section_2.select('div.item[style*="min-height: 58px;"]')

    for detail in country_details_list:
        country_name = detail.find('a', class_='country-name').text
        if country_name not in 'Sri Lanka':
            year_gdp = detail.find_all('div')
            year = year_gdp[1].text
            gdp = year_gdp[2].text
            print(f"Country Name: {country_name}| Year: {year}| GDP: {gdp}")
            print('')

def tradingeconomics():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
    url = 'https://tradingeconomics.com/sri-lanka/bank-lending-rate'
    driver.get(url)
    time.sleep(7)
    page_source = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_source, 'lxml')
    summary = soup.find('table', class_= 'table table-hover')
    
    # SUMMARY
    print(" ---------------------------------------------------------------- Rates ----------------------------------------------------------------")
    for row_data in summary.tbody.find_all('tr'):
        related = row_data.find('a').text.strip().replace('\t', '')
        values = row_data.find_all('td')
        last = values[1].text.strip().replace('\t', '')
        previous = values[2].text.strip().replace('\t', '')
        unit = values[3].text.strip().replace('\t', '')
        reference = values[4].text.strip().replace('\t', '')
        print(f"""
        Relate: {related}| Last: {last}| Previous: {previous}| Unit: {unit}| Reference: {reference}
        """)

    print(" ----------------------------------------------------- SRI LANKA PRIME LENDING RATE ----------------------------------------------------")
    # SRI LANKA PRIME LENDING RATE
    sl_lending_rate_info = soup.find('div', id = 'ctl00_ContentPlaceHolder1_ctl00_ctl01_Panel1')
    sl_lending_rate_table_info = sl_lending_rate_info.find_all('tbody')[0].find_all('td')
    actual_lending_rate = sl_lending_rate_table_info[1].text
    previous_lending_rate = sl_lending_rate_table_info[2].text
    highest_lending_rate = sl_lending_rate_table_info[3].text
    lowest_lending_rate = sl_lending_rate_table_info[4].text
    dates_lending_rate = sl_lending_rate_table_info[5].text
    untit_lending_rate = sl_lending_rate_table_info[6].text.strip().replace('\t', '')
    frequency_lending_rate = sl_lending_rate_table_info[7].text.strip().replace('\t', '')

    print(f"""
    Actual Lending Rate: {actual_lending_rate}
    Previous Lending Rate: {previous_lending_rate}
    Highest Lending Rate: {highest_lending_rate}
    Lowest Lending Rate: {lowest_lending_rate}
    Dates: {dates_lending_rate}
    Unit: {untit_lending_rate}
    Frequency: {frequency_lending_rate}
    """)

def parse_price_index(text):
    return re.search(r"(20\d{2})=(100|\d+)", text)

def extract_year_month_wise_price_indexes(row, section=None, year=None):
    if section:
        tds = row.find_all('td')
        colombo_price_index = tds[1].text
        national_price_index = tds[2].text
        colombo_price_index = parse_price_index(colombo_price_index)
        national_price_index = parse_price_index(national_price_index)
        colombo_year_of_price_index = colombo_price_index.group(1)
        colombo_price_index = colombo_price_index.group(2)
        national_year_of_price_index = national_price_index.group(1)
        national_price_index = national_price_index.group(2)
        section = False
        print(f"""
        Year: {colombo_year_of_price_index}
        Colombo Consumer Price Index(CCPI): {colombo_price_index}
        Year: {national_year_of_price_index}
        National Consumer Price Index (NCPI): {national_price_index}
        """)
        return section, year
    else:
        if "<strong><span" in str(row):
            year = row.find('span').text
            return section, year
        else:
            year = year
            row_detail = row.find_all('td')
            month = row_detail[0].text
            colombo_headine_inflation = row_detail[1].text
            colombo_core_inflation = row_detail[2].text
            national_headline_inflation = row_detail[3].text
            national_core_inflation = row_detail[4].text
            print(f"""
        ----------------------------------------------------------------------------------------
        Year: {year}
        Month: {month}
                                  Colombo Consumer Price Index(CCPI)     
        Headline Inflation: {colombo_headine_inflation}
        Core Inflation: {colombo_core_inflation}
        
                                  National Consumer Price Index (NCPI)
        Headline Inflation: {national_headline_inflation}
        Core Inflation: {national_core_inflation}
        ----------------------------------------------------------------------------------------
        """)
        return section, year
           
def check_status(color_name):
    if color_name == 'red':
        change_status = 'decreased'
    elif color_name == 'green':
        change_status = 'Increased'
    else:
        change_status = 'Not changed'
    
    return change_status

def cpi_ncpi():
    headers= {"accept-language": "en-US,en;q=0.9",
          "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}
    s = requests.Session()
    r = s.get(url='https://www.cbsl.gov.lk/cbsl_custom/inflation/inflationwindow.php', headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    section = True
    tables = soup.find_all("table")
    table_rows = tables[0].tbody.find_all('tr')
    year = None

    print(" ------------------------------------------------------------------------ CURRENT YEAR PRICE INDEXES ------------------------------------------------------------------------ ")
    # CURRENT YEAR PRICE INDEXES
    for row in table_rows:
        if "height: 45.0pt;" in row.get("style", ""):
            continue
        section, year = extract_year_month_wise_price_indexes(row, section, year)
        
    print('')
    print(" ------------------------------------------------------------------------ PREVIOUS YEAR PRICE INDEXES ------------------------------------------------------------------------ ")
    section = True
    # PREVIOUS YEAR PRICE INDEXES
    table_rows = tables[1].tbody.find_all('tr')
    for row in table_rows:
        if "height: 45.0pt;" in row.get("style", ""):
            continue
        section, year = extract_year_month_wise_price_indexes(row, section, year)

def get_cse_all_share_technical_analysis(html_page):
    soup = BeautifulSoup(html_page, 'lxml')
    div_element = soup.find('div', class_= 'flex flex-col items-center shrink text-center self-center ml-0 analyst-price-target_gaugeView__yP3BV !w-[300px]').find_all('div')
    return div_element[-1].text

def all_share_index():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
    url = 'https://www.investing.com/indices/cse-all-share'

    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    cse_all_sahre = soup.find('div', class_= 'text-5xl/9 font-bold md:text-[42px] md:leading-[60px] text-[#232526]').text.replace(',', '')
    instrument_price_change = soup.find('div', class_= 'flex gap-2 items-center text-base/6 font-bold md:text-xl/7 rtl:force-ltr text-negative-main').span.text
    invest_details = soup.find('dl', class_= 'flex-1').find_all('div', class_= 'flex flex-wrap items-center pt-2.5 sm:pb-2.5 justify-between border-t border-t-[#e6e9eb] pb-2.5')

    print('')
    print(' ------------------------------------------------------- SUMMARY ------------------------------------------------------- ')
    previous_close = invest_details[0].find('span', class_='key-info_dd-numeric__ZQFIs').text.replace(',', '')
    open = invest_details[1].find('span', class_='key-info_dd-numeric__ZQFIs').text.replace(',', '')
    year_1_change = invest_details[2].find('span', class_='key-info_dd-numeric__ZQFIs').text
    volume = invest_details[3].find('span', class_='key-info_dd-numeric__ZQFIs').text.replace(',', '')
    average_volume = invest_details[4].find('span', class_='key-info_dd-numeric__ZQFIs').text.replace(',', '')

    ranges = invest_details[5].find_all('span', class_='key-info_dd-numeric__ZQFIs')
    range1 = ranges[0].find_all('span')[1].text
    range2 = ranges[1].find_all('span')[1].text
    days_range = str(range1) + '-' + str(range2)

    ranges = soup.find('dl', class_= 'flex-1').find('div', class_= 'flex flex-wrap items-center pt-2.5 sm:pb-2.5 justify-between border-t border-t-[#e6e9eb] sm:border-b').find_all('span', class_='key-info_dd-numeric__ZQFIs')
    range1 = ranges[0].find_all('span')[1].text
    range2 = ranges[1].find_all('span')[1].text
    wk_52_range = str(range1) + '-' + str(range2)
    print(f"""
    Previous Close Amount: {previous_close}
    Open Amount: {open}
    1 Year Change Percentage: {year_1_change}
    Volume: {volume}
    Average Volume: {average_volume}
    Day's Range: {days_range}
    52 WK Range: {wk_52_range}
    """)
    print('')

    print(' ------------------------------------------------------- MARKETS ------------------------------------------------------- ')
    markets = soup.find('div', class_='mb-10', attrs={'data-test': 'quotes-box'}).find_all('div', attrs={'data-test': 'ws-markets-item'})
    start = True
    for market in markets:
        if start:
            rows = market.find('div', class_= 'table-row').find_all('div')
            market_name = rows[0].find('a', class_= 'text-ellipsis overflow-hidden hover:text-[#1256A0] hover:underline').text
            market_last_value = rows[1].text
            change = rows[2].span.text
            change_percentage = rows[3].span.text
            start = False
        else:
            row = market.find('div', class_= 'table-row').find_all('div')
            market_name = row[0].find('a', class_= 'text-ellipsis overflow-hidden hover:text-[#1256A0] hover:underline').text
            market_last_value = row[1].text
            change = row[2].find('span').text
            change_percentage = row[3].find('span').text
        print(f"""
        Market Name: {market_name}
        Market Last Value: {market_last_value}
        Change: {change}
        Change Percentage: {change_percentage}
        """)
    print('')
    print(' ------------------------------------------------------- ACTIVE STOCKS ------------------------------------------------------- ')
    active_stocks = soup.find('table', class_= 'w-full text-xs leading-4').find('tbody').find_all('tr', class_= 'hover:bg-[#F5F5F5] relative after:absolute after:bottom-0 after:bg-[#ECEDEF] after:h-px after:left-0 after:right-0')
    for active_stock in active_stocks:
        stock_name = active_stock.find('div', class_= 'flex items-center').find('span', class_= 'ml-1.5 font-semibold hover:text-[#1256A0] hover:underline text-ellipsis overflow-hidden').text
        company_name = active_stock.find('div', class_= 'mt-1 text-[#5B616E] hover:text-[#1256A0] hover:underline text-ellipsis overflow-hidden').text
        
        tds = active_stock.find_all('td', class_= 'align-top py-3 hidden md:table-cell md:align-middle md:text-right md:rtl:text-right')
        last = tds[0].text
        previous = tds[1].text
        high = tds[2].text
        low = tds[3].text
        change = active_stock.find('td', class_= 'align-top py-3 hidden md:table-cell md:align-middle md:text-right md:pl-4 md:rtl:text-right md:rtl:pl-4 md:rtl:pr-0').span.text
        volume = active_stock.find('td', class_= 'align-top py-3 md:align-middle md:text-right md:rtl:text-right').text
        timeofactivity = active_stock.find('td', class_= 'text-right py-3 rtl:soft-ltr flex pt-[13px] md:table-cell').span.span.text

        print(f"""
        Stock Name: {stock_name}
        Company Name: {company_name}
        Last: {last}
        Previous: {previous}
        High: {high}
        Low: {low}
        Change: {change}
        Volume: {volume}
        Time: {timeofactivity}
        """)

    print('')
    print(' ------------------------------------------------------- TOP GAINERS ------------------------------------------------------- ')
    active_stocks = soup.find_all('table', class_= 'w-full text-xs leading-4')[1].find('tbody').find_all('tr', class_= 'hover:bg-[#F5F5F5] relative after:absolute after:bottom-0 after:bg-[#ECEDEF] after:h-px after:left-0 after:right-0')
    for active_stock in active_stocks:
        gainer_name = active_stock.find('div', class_= 'flex items-center').find('span', class_= 'ml-1.5 font-semibold hover:text-[#1256A0] hover:underline text-ellipsis overflow-hidden').text
        company_name = active_stock.find('div', class_= 'mt-1 text-[#5B616E] hover:text-[#1256A0] hover:underline text-ellipsis overflow-hidden').text
        price = active_stock.find('td', class_= 'text-right py-3 pl-[30px] rtl:soft-ltr').span.text
        price_percentage = active_stock.find('td', class_= 'text-right py-3 pl-[30px] rtl:soft-ltr').span.text
        # volume = active_stock.find('td', class_= 'align-top py-3 md:align-middle md:text-right md:rtl:text-right').text
        # price = active_stock.find('td', class_= 'text-right py-3 pr-2 pl-[30px] rtl:soft-ltr md:hidden').find_all('span')[0].text
        # price_percentage = active_stock.find('td', class_= 'text-right py-3 pr-2 pl-[30px] rtl:soft-ltr md:hidden').find_all('span')[1].text
        print(f"""
        Top Gainer Name: {gainer_name}
        Company Name: {company_name}
        Price: {price}
        Price Percentage: {price_percentage}
        """)

    print('')
    print(' ------------------------------------------------------- TOP LOSERS ------------------------------------------------------- ')
    active_stocks = soup.find_all('table', class_= 'w-full text-xs leading-4')[2].find('tbody').find_all('tr', class_= 'hover:bg-[#F5F5F5] relative after:absolute after:bottom-0 after:bg-[#ECEDEF] after:h-px after:left-0 after:right-0')
    for active_stock in active_stocks:
        loser_name = active_stock.find('div', class_= 'flex items-center').find('span', class_= 'ml-1.5 font-semibold hover:text-[#1256A0] hover:underline text-ellipsis overflow-hidden').text
        company_name = active_stock.find('div', class_= 'mt-1 text-[#5B616E] hover:text-[#1256A0] hover:underline text-ellipsis overflow-hidden').text
        price = active_stock.find('td', class_= 'text-right py-3 pl-[30px] rtl:soft-ltr').span.text
        price_percentage = active_stock.find('td', class_= 'text-right py-3 pl-[30px] rtl:soft-ltr').span.text

        print(f"""
        Top Loser Name: {loser_name}
        Company Name: {company_name}
        Price: {price}
        Price Percentage: {price_percentage}
        """)

    print('')
    print(' ------------------------------------------------------- CSE ALL SHARE TECHNICAL ANALYSIS ------------------------------------------------------- ')

    driver.get("https://www.investing.com/indices/cse-all-share-technical")
    tab_indices = [0, 1, 2]  # Assuming 0 corresponds to DAILY, 1 to WEEKLY, and 2 to MONTHLY

    for tab_index in tab_indices:
        # Click on the corresponding tab
        link = driver.find_elements(By.CSS_SELECTOR, '[class*="inv-button inv-tab"]')[tab_index]
        driver.execute_script("arguments[0].click();", link)
        
        # Wait for some time (adjust as needed)
        time.sleep(5)
        
        # Get the page source
        html_page = driver.page_source
        
        # Perform analysis based on the tab
        if tab_index == 0:
            daily_cse_status = get_cse_all_share_technical_analysis(html_page)
        elif tab_index == 1:
            weekly_cse_status = get_cse_all_share_technical_analysis(html_page)
        elif tab_index == 2:
            monthly_cse_status = get_cse_all_share_technical_analysis(html_page)
    driver.close() 
    print(f"""
    Daily: {daily_cse_status}
    Weekly: {weekly_cse_status}
    Monthly: {monthly_cse_status}  
    """)

def no_of_teus():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
    # daily = driver
    url = 'https://www.ceicdata.com/en/indicator/sri-lanka/container-port-throughput'

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
    information_of_sl_container_throughput = ''
    uls = soup.find('div', attrs={"id": "left-col-7"}).ul.find_all('li')
    for ul in uls:
        information_of_sl_container_throughput += ul.text + '.'

    throuput_table = soup.find('table', class_= 'dp-table dp-table-auto').tbody.find('tr').find_all('td')
    last_throughput_amount = throuput_table[0].find_all('span')[0].text.strip().replace(',', '')
    last_throughput_year = throuput_table[0].find_all('span')[2].text

    previous_throughput_amount = throuput_table[1].find_all('span')[0].text.strip().replace(',', '')
    previous_throughput_year = throuput_table[1].find_all('span')[2].text

    min_throughput_amount = throuput_table[2].text.strip().replace(',', '')
    min_throughput_year = throuput_table[2].span.text

    max_throughput_amount = throuput_table[3].text.strip().replace(',', '')
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

    tb_rows = soup.find('div', attrs= {'id': 'ipc-table-countries'}).find('table', class_= 'dp-table').tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        country_region = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
        last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
        last_year = get_row_info[1].find_all('span')[2].text.strip()
        container_port_throughput_frequency = get_row_info[2].text.strip()
        container_port_throughput_range = get_row_info[3].text.strip()
        print(f"""
        Country: {country_region}
        Last Amount: {last_amount}
        Change_Status: {change_status}
        Last Amount Year: {last_year}
        Frequency: {container_port_throughput_frequency}
        Range: {container_port_throughput_range}
        """)
    print('')
    print(' --------------------------------------------------------------- SL Key Series --------------------------------------------------------------- ')
    # tb_rows = soup.find('div', attrs= {'id': 'ipc-table-categories'}).find('table', class_= 'dp-table').tbody.find_all('tr')
    tables = soup.find('div', attrs= {'id': 'ipc-table-categories'}).find_all('table', class_= 'dp-table')
    tb_rows = tables[0].tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        g_p_finance_name = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
        last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
        last_year = get_row_info[1].find_all('span')[2].text.strip()
        frequency = get_row_info[2].text.strip()
        range = get_row_info[3].text.strip()
        print(f"""
        Government And Public Finance: {g_p_finance_name}
        Last Amount: {last_amount}
        Change_Status: {change_status}
        Last Amount Year: {last_year}
        Frequency: {frequency}
        Range: {range}
        """)

    print('')
    print(' --------------------------------------------------------------- FOREIGN TRADE --------------------------------------------------------------- ')
    tables = soup.find('div', attrs= {'id': 'ipc-table-categories'}).find_all('table', class_= 'dp-table')
    tb_rows = tables[1].tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        foreign_trade_name = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
        last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
        last_year = get_row_info[1].find_all('span')[2].text.strip()
        frequency = get_row_info[2].text.strip()
        range = get_row_info[3].text.strip()
        print(f"""
        Foreign Trade: {foreign_trade_name}
        Last Amount: {last_amount}
        Change_Status: {change_status}
        Last Amount Year: {last_year}
        Frequency: {frequency}
        Range: {range}
        """)

    print('')
    print(' --------------------------------------------------------------- BALANCE OF PAYMENTS --------------------------------------------------------------- ')
    tables = soup.find('div', attrs= {'id': 'ipc-table-categories'}).find_all('table', class_= 'dp-table')
    tb_rows = tables[2].tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        balance_of_payments = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
        last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
        last_year = get_row_info[1].find_all('span')[2].text.strip()
        frequency = get_row_info[2].text.strip()
        range = get_row_info[3].text.strip()
        print(f"""
        Balance of Payments: {balance_of_payments}
        Last Amount: {last_amount}
        Change_Status: {change_status}
        Last Amount Year: {last_year}
        Frequency: {frequency}
        Range: {range}
        """)

    print('')
    print(' --------------------------------------------------------------- MONETARY --------------------------------------------------------------- ')
    tables = soup.find('div', attrs= {'id': 'ipc-table-categories'}).find_all('table', class_= 'dp-table')
    tb_rows = tables[3].tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        monetary_trade_name = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
        last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
        last_year = get_row_info[1].find_all('span')[2].text.strip()
        frequency = get_row_info[2].text.strip()
        range = get_row_info[3].text.strip()
        print(f"""
        Monetary: {monetary_trade_name}
        Last Amount: {last_amount}
        Change_Status: {change_status}
        Last Amount Year: {last_year}
        Frequency: {frequency}
        Range: {range}
        """)

    print('')
    print(' --------------------------------------------------------------- BUSINESS AND ECONOMIC SURVEY --------------------------------------------------------------- ')
    tables = soup.find('div', attrs= {'id': 'ipc-table-categories'}).find_all('table', class_= 'dp-table')
    tb_rows = tables[4].tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        business_and_economic_survey = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
        last_amount = get_row_info[1].find_all('span')[0].text.strip().replace(',', '')
        last_year = get_row_info[1].find_all('span')[2].text.strip()
        frequency = get_row_info[2].text.strip()
        range = get_row_info[3].text.strip()
        print(f"""
        Business And Economic Survey: {business_and_economic_survey}
        Last Amount: {last_amount}
        Change_Status: {change_status}
        Last Amount Year: {last_year}
        Frequency: {frequency}
        Range: {range}
        """)

    print('')
    print(' --------------------------------------------------------------- INDICATORS FOR SRI LANKA --------------------------------------------------------------- ')
    tb_rows = soup.find('div', attrs= {'id': 'left-col-7'}).find_all('div', attrs= {'id': 'op-table-related'})[-1].find('table', class_= 'dp-table').tbody.find_all('tr')
    for row in tb_rows:
        get_row_info = row.find_all('td')
        indicator = get_row_info[0].a.text.strip()
        last_color = get_row_info[1].find_all('span')[0].get('class')
        last_amount_status = re.search(r'c-(\w+)', ' '.join(last_color))
        color_name = last_amount_status.group(1) if last_amount_status else None
        change_status = check_status(color_name)
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

def tourist_arrivals():
    url = 'https://www.sltda.gov.lk/en/monthly-tourist-arrivals-reports-2023'

    html_page = requests.get(url).text

    soup = BeautifulSoup(html_page, 'lxml')
    table_rows = soup.find('div', class_= 'col-xl-10 offset-xl-1 col-lg-12 offset-lg-0 col-md-12 offset-md-0 register-back-wrap short-code-text downloads-table').find('table').tbody.find_all('tr')[1:]
    # headers = soup.find('div', class_= 'col-xl-10 offset-xl-1 col-lg-12 offset-lg-0 col-md-12 offset-md-0 register-back-wrap short-code-text downloads-table').find('table').tbody.find_all('tr')[0].find_all('td')
    # header_1 = headers[0].td.text
    for row in table_rows:
        row_details = row.find_all('td')
        month = row_details[0].text
        previous_year_amount = row_details[1].text.replace(',', '')
        current_year_amount = row_details[2].text.replace(',', '')
        percentage_between_previous_and_now = row_details[3].text
        
        print(f"""
        Month: {month}
        Previous Year Amount: {previous_year_amount}
        Current Year Amount: {current_year_amount}
        % Cha. Percentage Between Previous And Now: {percentage_between_previous_and_now}
        """)

def logistics_performance_index():
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
        change_status = check_status(color_name)
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
        change_status = check_status(color_name)
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
        change_status = check_status(color_name)
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
        change_status = check_status(color_name)
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
        change_status = check_status(color_name)
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
        change_status = check_status(color_name)
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
        change_status = check_status(color_name)
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
