import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def create_folder(keyword):
    """Create folder for keyword if it doesn't exist"""
    folder_name = ''.join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def download_image(img_url, folder_path, filename):
    """Download and save an image"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(img_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Clean filename
        clean_name = ''.join(c for c in filename if c.isalnum() or c in ('-', '_')).rstrip()
        filepath = os.path.join(folder_path, f"{clean_name}.jpg")
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")
        return True
    except Exception as e:
        print(f"Error downloading {img_url}: {str(e)}")
        return False

def scrape_images(keyword, num_images=10):
    """Scrape images from Google Images for given keyword"""
    search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&tbm=isch"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        folder_path = create_folder(keyword)
        downloaded_count = 0
        
        for img_tag in soup.find_all('img'):
            if downloaded_count >= num_images:
                break
                
            img_url = img_tag.get('src')
            if img_url and img_url.startswith('http'):
                filename = f"{keyword}_{downloaded_count+1}"
                if download_image(img_url, folder_path, filename):
                    downloaded_count += 1
                    time.sleep(1)  # Be polite to the server
        
        print(f"Downloaded {downloaded_count} images for '{keyword}'")
        
    except Exception as e:
        print(f"Error scraping {keyword}: {str(e)}")

def main():
    # Read keywords from text file
    try:
        with open('scrape/keywords.txt', 'r') as file:
            keywords = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: keywords.txt file not found!")
        return

    # Scrape images for each keyword
    for keyword in keywords:
        print(f"\nScraping images for: {keyword}")
        scrape_images(keyword, num_images=5)  # Change num_images as needed

if __name__ == "__main__":
    main()