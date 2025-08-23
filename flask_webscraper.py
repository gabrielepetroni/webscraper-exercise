
from flask import Flask
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
T_URL = "https://www.apple.com"

app = Flask(__name__)

@app.route('/firstfilter')
def index():
    return 'Index Page'

@app.route('/secondfilter')
def hello():
    return 'Hello, World'
