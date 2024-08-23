import random
import re
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


# List of user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def search_companyname(driver, stock_name):
    try:
        driver.get('https://fr.finance.yahoo.com/lookup')
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="btn secondary reject-all"]'))).click()

        search_bar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "yfin-usr-qry")))
            
        search_bar.send_keys(stock_name)
        first_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//li[@class="modules-module_linkItem__r-Zwd modules-module_quoteItem__W8hI- modules-module_selectedBackground__6dnU7"]')))

        symbols = driver.find_elements(By.CLASS_NAME, 'modules-module_quoteSymbol__BGsyF')
        company_names = driver.find_elements(By.CLASS_NAME, 'modules-module_quoteCompanyName__JVZCM')
        quote_spans = driver.find_elements(By.CLASS_NAME, 'modules-module_quoteSpan__0xMtT')

        data = []
        for symbol, company_name, quote_span in zip(symbols, company_names, quote_spans):
            data.append([symbol.text, company_name.text, quote_span.text])

        df = pd.DataFrame(data, columns=['Symbol', 'Company Name', 'Quote Span'])
        return (df)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def check_ticker(ticker):
    try:
        info = yf.Ticker(ticker).info
        return 'longBusinessSummary' in info and info.get('exchange') != 'PNK'
    except Exception as e:
        return False

def df_stock(stock_name):
    
    start_time = time.time()
    driver = get_driver()
    df = search_companyname(driver, stock_name)
    driver.quit()
    end_time = time.time()

    print(f"Total time taken for scraping: {round(end_time - start_time,2)} seconds")
    df_filtered = df[df["Symbol"].apply(check_ticker)]
    df_filtered.loc[:, "Quote Span"] = df_filtered["Quote Span"].str.replace("Titres - ", "", regex=False)
    df_filtered = df_filtered.rename(columns={
        "Symbol": "Ticker",
        "Company Name": "Company Name",
        "Quote Span": "Exchange"
    })
    return df_filtered[["Ticker", "Company Name", "Exchange"]]

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)

    # Basic Information
    name = stock.info.get('longName', 'N/A')
    country = stock.info.get('country', 'N/A')
    industry = stock.info.get('industry', 'N/A')
    sector = stock.info.get('sector', 'N/A')
    business_summary = stock.info.get('longBusinessSummary', 'N/A')
    
    sentences = business_summary.split('. ')
    shortened_text = '. '.join(sentences[:2]) + '.'
    exchange = stock.info.get('exchange', 'N/A')

    # Stock Prices
    open_price = stock.info.get('open', 'N/A')
    high_price = stock.info.get('dayHigh', 'N/A')
    low_price = stock.info.get('dayLow', 'N/A')
    close_price = stock.info.get('previousClose', 'N/A')


    # Target Prices
    current_price = stock.info.get('currentPrice', 'N/A')
    target_high_price = stock.info.get('targetHighPrice', 'N/A')
    target_low_price = stock.info.get('targetLowPrice', 'N/A')
    target_mean_price = stock.info.get('targetMeanPrice', 'N/A')
    target_median_price = stock.info.get('targetMedianPrice', 'N/A')

    # Additional Information
    quote_type = stock.info.get('quoteType', 'N/A')
    symbol = stock.info.get('symbol', 'N/A')
    currency = stock.info.get('currency', 'N/A')
    beta = stock.info.get('beta', 'N/A')

    # Recommendation
    recommendation_key = stock.info.get('recommendationKey', 'N/A')
    recommendation_nb = stock.info.get('numberOfAnalystOpinions', 'N/A')

    return {
        'Name': name,
        'Symbol': symbol,
        'Quote Type': quote_type,
        'Country': country,
        'Industry': industry,
        'Sector': sector,
        'Business Summary': shortened_text,
        'Exchange': exchange,
        'Currency': currency,
        'Current Price': current_price,
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Target High Price': target_high_price,
        'Target Low Price': target_low_price,
        'Target Mean Price': target_mean_price,
        'Target Median Price': target_median_price,
        'Beta': beta,
        'Recommendation': recommendation_key,
        '# of analyst opinions': recommendation_nb
    }

def get_long_name_ticker(driver, stock_name):
    try:
        driver.get('https://fr.finance.yahoo.com/lookup')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="btn secondary reject-all"]'))).click()
        SearchBar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "yfin-usr-qry")))
        SearchBar.send_keys(stock_name)
        
        first_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//li[@class="modules-module_linkItem__r-Zwd modules-module_quoteItem__W8hI- modules-module_selectedBackground__6dnU7"]')))
        first_element.click()

        stock_info_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//h1[@class="D(ib) Fz(18px)"]')))
        stock_info_text = stock_info_element.text
        match = re.search(r'([^()]+)\s+\(([^)]+)\)', stock_info_text)
        long_name = match.group(1).strip() if match else None
        ticker = match.group(2) if match else None
        return long_name, ticker
    
    except Exception as e:
        print(f"An error occurred while retrieving long name and ticker: {e}")
        return None, None

def get_latest_news(driver, ticker_name, long_name):
    try:
        news_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Tous"]')))
        news_tab.click()
    except Exception as e:
        print(f"Failed to click on the news tab: {e}")
        return pd.DataFrame(columns=['Date', 'Author', 'Title', 'Href'])  


    terms_to_check = [ticker_name] + [word.capitalize() for word in long_name.split() if len(word) > 2]

    articles_data = []

    article_items = driver.find_elements(By.CLASS_NAME, "js-stream-content")
    if not article_items:
        print("No articles found.")
        return pd.DataFrame(columns=['Date', 'Author', 'Title', 'Href']) 

    for article_item in article_items:
        try:
            title_link = article_item.find_element(By.XPATH, './/h3/a')
            description_element = article_item.find_element(By.XPATH, './/p')
            found_in_title = any(term.lower() in title_link.text.lower() for term in terms_to_check)
            found_in_description = any(term.lower() in description_element.text.lower() for term in terms_to_check)
            
            if found_in_title or found_in_description:
                author_and_date_div = article_item.find_element(
                    By.XPATH, './/div[@class="C(#959595) Fz(11px) D(ib) Mb(6px)"]')
                author, date = [span.text.strip() for span in author_and_date_div.find_elements(
                    By.XPATH, './span')[:2]]
                title = title_link.text.strip()
                href = title_link.get_attribute("href")
                articles_data.append(
                    {'Date': date, 'Author': author, 'Title': title, 'Href': href})
        except Exception as e:
            print(f"An error occurred while processing an article item: {e}")
            continue  

    return pd.DataFrame(articles_data)

def save_news_to_excel(news_df, ticker):
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{current_datetime}_{ticker}_news.xlsx"
    os.makedirs("output/news/", exist_ok=True)
    news_df.to_excel(f"output/news/{file_name}", index=False)


def get_company_news(stock_name, save_to_excel=True):
    start_time = time.time()
    driver = get_driver()
    long_name, ticker_name = get_long_name_ticker(driver, stock_name)
    news_df = get_latest_news(driver, ticker_name, long_name)
    driver.quit()
    end_time = time.time()
    print(f"Total time taken for scraping: {end_time - start_time} seconds")
    if save_to_excel:
        save_news_to_excel(news_df, ticker_name)
    return news_df

