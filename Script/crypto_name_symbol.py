from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
def main():
    print("====================Fetching data====================")
    driver = webdriver.Chrome()
    url = "https://finance.yahoo.com/markets/crypto/all/"
    driver.get(url)
    # Wait for the table to load
    
    table = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='markets-table freeze-col yf-paf8n5 fixedLayout']"))
    )

    html_content = driver.page_source
    driver.quit()

    soup = bs(html_content, 'lxml')
    table = soup.find('table', class_='markets-table freeze-col yf-paf8n5 fixedLayout')

    table_header = (table.find('thead')).find_all('th')

    table_header = [table_header[i].get_text(strip=True) for i in range(len(table_header)) if i not in (2,len(table_header)-1)]

    table_header.insert(1, 'Image URLS')


    data = []
   
   #for top 15 cryptos
    for table_row in table.find('tbody').find_all('tr')[:10]:

        cells = table_row.find_all('td')
        # Get the first <td> element's text, or return NaN if not found
        sym = cells[0].get_text(strip=True)
        sym = sym.split()

        sym = sym[0] if len(sym)==1 else sym[1]

        # Get the image's 'src' attribute, or return NaN if <img> or 'src' not found
        img_src = table_row.find('img').get("src") if table_row.find('img') else None
        name = table_row.find_all('td')[1].get_text(strip=True)

        # The third column contains the text "Price","Change", and "Change %"
        col_3 = cells[3].text.strip().split()

        # Get other columns' text, or return NaN if not found
        other_columns = [cells[i].get_text(strip=True) for i in range(6, len(cells)-1)]

        row_data = [sym, img_src, name] + col_3 + other_columns
        data.append(row_data)

    print("====================Data fetched ====================")
    df = pd.DataFrame(data=data, columns=table_header)
   
    print("====================Dataframe created ====================")
    df.to_csv("crypto_name_symbol.csv", index=False)




if __name__ == "__main__":
    main()