
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

# Flask web app initialization
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/firstfilter')
def firstfilter():
    entries = data_retrieval()

    entries = [entry for entry in entries if len(entry["title"].split(' ')) >= 6]
    
    entries = sorted(entries, key=lambda x: int(x['ncomments']), reverse=True)

    return render_template('dataviz.html', entries=entries, isfirsttask=True)

@app.route('/secondfilter')
def secondfilter():
    entries = data_retrieval()

    entries = [entry for entry in entries if len(entry["title"].split(' ')) <= 5]
    
    entries = sorted(entries, key=lambda x: int(x['score']), reverse=True)

    return render_template('dataviz.html', entries=entries, isfirsttask=False)

def data_retrieval():
    # Page entries list
    entries = []
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
        entry["ncomments"] = "0" if not entry["ncomments"].isnumeric() else entry["ncomments"]
        # Print each entry for debugging
        print(entry["id"]+" - "+entry["title"]+" - "+entry["score"]+" - "+entry["ncomments"])

        # Append entry to entries list
        entries.append(entry)

    driver.quit()
    return entries

if __name__ == '__main__':
   app.run()