import json
import re

def download_images_enhanced(url, folder_name="downloaded_images", max_images=50):
    """Enhanced version that looks for images in JavaScript data."""
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Could not retrieve the webpage - {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Method 1: Regular img tags
    img_tags = soup.find_all('img')
    img_urls = []
    
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if img_url:
            img_urls.append(urljoin(url, img_url))
    
    # Method 2: Look for JSON data with images
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string:
            # Look for JSON patterns
            json_matches = re.findall(r'\{[^{}]*"images"[^{}]*\}', script.string)
            for match in json_matches:
                try:
                    data = json.loads(match)
                    if 'images' in data and isinstance(data['images'], list):
                        for img_data in data['images']:
                            if isinstance(img_data, str):
                                img_urls.append(urljoin(url, img_data))
                except:
                    pass
    
    # Method 3: Look for background images in CSS
    elements_with_bg = soup.find_all(style=re.compile(r'background-image:\s*url'))
    for element in elements_with_bg:
        style = element.get('style', '')
        bg_match = re.search(r'background-image:\s*url\([\'"]?(.*?)[\'"]?\)', style)
        if bg_match:
            img_urls.append(urljoin(url, bg_match.group(1)))
    
    # Remove duplicates
    img_urls = list(set(img_urls))
    print(f"Found {len(img_urls)} unique image URLs")
    
    # Download images
    os.makedirs(folder_name, exist_ok=True)
    downloaded_count = 0
    
    for i, img_url in enumerate(img_urls):
        if downloaded_count >= max_images:
            break
            
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
            print(f"Failed to download {img_url}: {e}")
            continue
    
    print(f"\nDownloaded {downloaded_count} images to '{folder_name}' folder")