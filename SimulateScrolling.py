from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

def download_images_with_scroll(url, folder_name="downloaded_images", max_images=50):
    """Download images with scrolling to load lazy-loaded content."""
    
    # Set up Chrome driver (you'll need to install chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Scroll to bottom multiple times to trigger lazy loading
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        
        while scroll_attempts < 5:  # Limit scroll attempts
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # No more content to load
            last_height = new_height
            scroll_attempts += 1
        
        # Now find all images
        img_elements = driver.find_elements(By.TAG_NAME, 'img')
        print(f"Found {len(img_elements)} images after scrolling")
        
        # Create directory
        os.makedirs(folder_name, exist_ok=True)
        
        downloaded_count = 0
        for i, img in enumerate(img_elements):
            if downloaded_count >= max_images:
                break
                
            img_url = img.get_attribute('src') or img.get_attribute('data-src')
            if not img_url:
                continue
                
            try:
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()
                
                # Get file extension
                ext = os.path.splitext(img_url.split('?')[0])[1]
                if not ext:
                    content_type = img_response.headers.get('content-type', '')
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        ext = '.jpg'
                    elif 'png' in content_type:
                        ext = '.png'
                    elif 'gif' in content_type:
                        ext = '.gif'
                    else:
                        continue
                
                filename = os.path.join(folder_name, f"image_{downloaded_count+1:03d}{ext}")
                
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"Downloaded: {filename}")
                downloaded_count += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Failed to download image {i+1}: {e}")
                continue
                
    finally:
        driver.quit()
    
    print(f"\nDownloaded {downloaded_count} images to '{folder_name}' folder")