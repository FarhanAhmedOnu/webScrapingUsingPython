import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time

def is_valid_url(url):
    """Validate if the provided URL is well-formed."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_images(url, folder_name="downloaded_images", max_images=10):
    """Download images from a given URL."""
    if not is_valid_url(url):
        print("Error: Invalid URL provided.")
        return

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Could not retrieve the webpage - {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    if not img_tags:
        print("No images found on the page.")
        return

    # Create directory if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    downloaded_count = 0
    for img in img_tags:
        if downloaded_count >= max_images:
            break

        img_url = img.get('src') or img.get('data-src')  # Handle lazy-loaded images
        if not img_url:
            continue

        # Convert relative URLs to absolute URLs
        img_url = urljoin(url, img_url)

        try:
            img_response = requests.get(img_url, timeout=10)
            img_response.raise_for_status()

            # Get file extension from URL or content-type header
            ext = os.path.splitext(img_url)[1]
            if not ext:
                content_type = img_response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                else:
                    continue  # Skip unknown formats

            filename = os.path.join(folder_name, f"image_{downloaded_count+1:03d}{ext}")
            
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            
            print(f"Downloaded: {filename}")
            downloaded_count += 1
            time.sleep(0.5)  # Be respectful to the server

        except requests.RequestException as e:
            print(f"Failed to download {img_url}: {e}")
            continue

    print(f"\nDownloaded {downloaded_count} images to '{folder_name}' folder")

if __name__ == "__main__":
    url = input("Enter the URL to scrape images from: ").strip()
    try:
        max_count = int(input("Enter maximum number of images to download (default 10): ") or 10)
    except ValueError:
        max_count = 10
    
    folder = input("Enter folder name for images (default 'downloaded_images'): ").strip() or "downloaded_images"
    
    download_images(url, folder, max_count)