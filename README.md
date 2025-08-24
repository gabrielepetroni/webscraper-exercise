# Web-scraper Exercise
Developed by Gabriele Petroni as part of Stack Builder's hiring process.

## Scope

The goal of this exercise is to scrape data from the website [Hacker News](https://news.ycombinator.com) and apply filtering techniques to retrieve specific data and order it by the given criteria. It is possible to visualize said data as an HTML webpage using a web browser.

## Usage
Install the required packages from requirements.txt file; then run the Flask app
```
$ pip install -r requirements.txt
$ python3 flask_webscraper.py
```

A development server should be running by default on http://127.0.0.1:5000; if not, check your system configuration and available ports.

## Code structure
The application front-end and interactive part for the user has been designed as a webapp running on Flask. 
Once the user opens the main web-page, it is presented with two buttons pointing to two different pages representing the two different filters/queries to be applied to the retrieved data. To make the interface user-friendly and visually appealing rather than plain HTML, Bootrstrap has been used to organize the layout, fonts and custom components. Jinja templates are used to display the information dinamically: a single 'dataviz.html' has been designed for both the first and second filter as it adapts dinamically depending on the render request.
<br>
The backend part consists of a data retrieving + filtering section made using Selenium and the Chrome webdriver to access the webpage and retrive its data. Selenium has been used instead of the standard 'requests' package to allow for dynamic content to load. The raw HTML content is the parsed using BeautifulSoup4 and its content filtered using the same library functions.
Additional filtering is then made depending on the loaded page and its corresponding filter; fresh data is always downloaded on each page refresh to ensure the content stays updated.

