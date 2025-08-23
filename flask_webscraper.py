
from flask import Flask, render_template
import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import pandas as pd
from pathlib import Path
from zoneinfo import ZoneInfo

# Target URL
T_URL = "https://news.ycombinator.com"

# Page entries
entries = []

# Flask web app initialization
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/firstfilter')
def firstfilter():
    data_retrieval()
    return render_template('dataviz.html', entries=entries)

@app.route('/secondfilter')
def secondfilter():
    data_retrieval()
    return render_template('dataviz.html', entries=entries)

def data_retrieval():
    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the target URL
    driver.get(T_URL)

    # Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract data 
    rows = soup.find_all('tr', class_='athing submission')
    for row in rows:
        # Create empty entry dictionary
        entry = {}
        entry["id"] = row.find('span', class_='rank').text.strip('.')
        entry["title"] = row.find('span', class_='titleline').text
        entry["score"] = row.find_next_sibling('tr').find('span', class_='score').text.strip(' points') if row.find_next_sibling('tr').find('span', class_='score') else '0 points'.strip(' points')
        entry["ncomments"] = row.find_next_sibling('tr').find_all('a')[-1].text.strip(' comments') if row.find_next_sibling('tr').find_all('a') else '0 comments'.strip(' comments')
        # Print each entry for debugging
        print(entry["id"]+" - "+entry["title"]+" - "+entry["score"]+" - "+entry["ncomments"])

        # Append entry to entries list
        entries.append(entry)

    driver.quit()

if __name__ == '__main__':
   print(data_retrieval())
   #app.run()