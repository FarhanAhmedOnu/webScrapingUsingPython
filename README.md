# Image Scraper Collection

A collection of Python scripts for scraping images from various sources including Google Images and general websites.

## Technologies Used

- **Python 3**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **Selenium** - Web automation and scrolling simulation
- **ChromeDriver** - Browser automation (for scrolling functionality)

## Installation

1. Install required packages:
```bash
pip install requests beautifulsoup4 selenium
```

2. Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) and ensure it's in your system PATH.

## Usage

### 1. Google Images Scraper (`google.py`)
Scrapes images from Google Images using keywords.
```bash
python google.py
```
- Requires `scrape/keywords.txt` file with one keyword per line
- Downloads 5 images per keyword by default

### 2. General Website Scraper (`scrapeAnyWebsite.py`)
Scrapes images from any website URL.
```bash
python scrapeAnyWebsite.py
```
- Prompts for URL, image count, and folder name
- Supports both standard and scroll-enhanced versions

### 3. Enhanced Scraper (`enhancedScrape.py`)
Advanced scraper that detects images in JavaScript data, JSON, and CSS backgrounds.

### 4. Scrolling Simulator (`SimulateScrolling.py`)
Uses Selenium to simulate scrolling and load lazy-loaded images with size filtering.

## File Structure

- `google.py` - Google Images scraper
- `scrapeAnyWebsite.py` - General website scraper
- `enhancedScrape.py` - Enhanced scraping with multiple detection methods
- `SimulateScrolling.py` - Scroll simulation for dynamic content
- `find_image_endpoints.py` - API endpoint discovery
- `keywords.txt` - Keywords for Google scraping

## Features

- Multiple image detection methods
- Lazy-loading support with scrolling
- Image size filtering
- Duplicate removal
- Respectful crawling with delays
- Automatic folder creation
- Error handling and logging

## Notes

- Respect website terms of service and robots.txt
- Adjust delays to avoid overloading servers
- Some websites may require additional headers or authentication
- ChromeDriver must be installed for scrolling functionality
