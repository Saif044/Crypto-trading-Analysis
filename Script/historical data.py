from datetime import datetime, timedelta
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd



#================================= Convert datetime to Unix timestamp===========================
def datetime_to_unix(date):
    return int(time.mktime(date.timetuple()))

def get_html_content(symbol):
    #=======================Define the date range for the historical data=====================
    today = datetime.now()
    one_year_ago = (datetime.now() - timedelta(days=365))
    #========================get historical data=======================================
    link = f"https://finance.yahoo.com/quote/{symbol}/history/?period1={datetime_to_unix(one_year_ago)}&period2={datetime_to_unix(today)}"

    driver = webdriver.Chrome()
    driver.get(link)
    # Wait for the table to load
    table_wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='nimbus-app']/section/section/section/article/div[1]/div[3]/table")))
    
    html_content = driver.page_source
    driver.quit()
    return bs(html_content, 'lxml')

def header_and_symbol():    
    #=======================get crypto name and symbol=======================================
    sym = pd.read_csv('crypto_name_symbol.csv')
    symbols = sym['Symbol'].tolist()
    table_head= ['Date', 'Open', 'High', 'Low', 'Close', 'Adj', 'Volume', 'Symbol']
    return symbols, table_head

def main():
    data = []
    symbols, table_head = header_and_symbol()

    #=======================fetching data=======================================
    for symbol in symbols:
        print(symbol)
        page = get_html_content(symbol)
        table = page.find('table', class_='table yf-1jecxey noDl')
        table_rows = table.find('tbody').find_all('tr')

        for d in table_rows:
            td = d.find_all('td')
            row_data  = [i.text.strip() for i in td]
            row_data.append(symbol)
            data.append(row_data)
    #=======================Creating dataframe=======================================
    df = pd.DataFrame(data=data, columns=table_head)
    df.to_csv("historical_data.csv", index=False)






if __name__ == "__main__":
    main()
    print("Done")
    