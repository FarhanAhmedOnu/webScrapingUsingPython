from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

def download_images_with_scroll(url, folder_name="downloaded_images", max_images=50, min_size_kb=10):
    """Download images with scrolling to load lazy-loaded content, filtering by minimum size."""
    
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
            new_height = driver.execute_script("return document.body.scrollHeight")  # FIXED: execute_script not execute_cript
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
        skipped_small_count = 0
        
        for i, img in enumerate(img_elements):
            if downloaded_count >= max_images:
                break
                
            img_url = img.get_attribute('src') or img.get_attribute('data-src')
            if not img_url:
                continue
                
            try:
                # Get the image with stream to check size before downloading completely
                img_response = requests.get(img_url, timeout=10, stream=True)
                img_response.raise_for_status()
                
                # Get content length from headers
                content_length = img_response.headers.get('content-length')
                if content_length:
                    size_kb = int(content_length) / 1024
                    if size_kb < min_size_kb:
                        print(f"Skipped small image ({size_kb:.1f}KB): {img_url[:80]}...")
                        skipped_small_count += 1
                        continue
                
                # If no content-length header, download and check size
                img_content = img_response.content
                size_kb = len(img_content) / 1024
                
                if size_kb < min_size_kb:
                    print(f"Skipped small image ({size_kb:.1f}KB): {img_url[:80]}...")
                    skipped_small_count += 1
                    continue
                
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
                    elif 'webp' in content_type:
                        ext = '.webp'
                    else:
                        print(f"Skipped unknown format: {content_type}")
                        continue
                
                filename = os.path.join(folder_name, f"image_{downloaded_count+1:03d}{ext}")
                
                # Save the image
                with open(filename, 'wb') as f:
                    f.write(img_content)
                
                print(f"Downloaded: {filename} ({size_kb:.1f}KB)")
                downloaded_count += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Failed to download image {i+1}: {e}")
                continue
                
    finally:
        driver.quit()
    
    print(f"\nDownloaded {downloaded_count} images to '{folder_name}' folder")
    print(f"Skipped {skipped_small_count} images that were smaller than {min_size_kb}KB")

# Updated main function to accept minimum size parameter
if __name__ == "__main__":
    url = input("Enter the URL to scrape images from: ").strip()
    try:
        max_count = int(input("Enter maximum number of images to download (default 50): ") or 50)
    except ValueError:
        max_count = 50
    
    folder = input("Enter folder name for images (default 'downloaded_images'): ").strip() or "downloaded_images"
    
    try:
        min_size = int(input("Enter minimum image size in KB (default 10): ") or 10)
    except ValueError:
        min_size = 10
    
    download_images_with_scroll(url, folder, max_count)