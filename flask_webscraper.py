
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os



# Target URL
T_URL = "https://news.ycombinator.com"

def remove_non_alnumeric(list):
    return [''.join(filter(str.isalnum, item)) for item in list]
    

# Flask web app initialization
app = Flask(__name__)

@app.route('/')
def index():
      return render_template('index.html')

# First task: filter entries with more than 5 words in the title and sort by number of comments
@app.route('/firstfilter')
def firstfilter():
    # Retrieve entries
    entries = data_retrieval()

    # Filter entries with more than 5 words in the title
    entries = [entry for entry in entries if len(remove_non_alnumeric(entry['title'].split(" ")))  >= 6]

    # Sort entries by number of comments in descending order
    entries = sorted(entries, key=lambda x: int(x['ncomments']), reverse=True)

    # Render the dataviz template with the filtered and sorted entries
    return render_template('dataviz.html', entries=entries, isfirsttask=True)

# Second task: filter entries with 5 or less words in the title and sort by score
@app.route('/secondfilter')
def secondfilter():
    # Retrieve entries
    entries = data_retrieval()

    # Filter entries with 5 or less words in the title
    entries = [entry for entry in entries if len(remove_non_alnumeric(entry['title'].split(" "))) <= 5] 

    # Sort entries by score in descending order
    entries = sorted(entries, key=lambda x: int(x['score']), reverse=True)

    # Render the dataviz template with the filtered and sorted entries
    return render_template('dataviz.html', entries=entries, isfirsttask=False)

def data_retrieval():
    # Page entries list
    entries = []
    # Set up headless Chrome using Selenium
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the target URL
    driver.get(T_URL)

    # Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract data 
    rows = soup.find_all('tr', class_='athing submission')
    for row in rows:
        # Create empty entry dictionary, collecting only the required fields
        entry = {}
        entry["id"] = row.find('span', class_='rank').text.strip('.')
        entry["title"] = " ".join(row.find('span', class_='titleline').text.split(" ")[:-1])
        entry["score"] = row.find_next_sibling('tr').find('span', class_='score').text.strip(' points') if row.find_next_sibling('tr').find('span', class_='score') else '0 points'.strip(' points')
        entry["ncomments"] = row.find_next_sibling('tr').find_all('a')[-1].text.strip(' comments') if row.find_next_sibling('tr').find_all('a') else '0 comments'.strip(' comments')
        # additional check to ensure alphanumeric values for the comment field
        entry["ncomments"] = "0" if not entry["ncomments"].isnumeric() else entry["ncomments"]
        # Print each entry for debugging
        print(entry["id"]+" - "+entry["title"]+" - "+entry["score"]+" - "+entry["ncomments"])

        # Append entry to entries list
        entries.append(entry)

    driver.quit()
    return entries

if __name__ == '__main__':
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)