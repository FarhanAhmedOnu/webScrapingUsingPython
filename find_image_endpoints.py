import requests
from bs4 import BeautifulSoup

def find_image_endpoints(url):
    """Try to find API endpoints that serve images."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Could not retrieve the webpage - {e}")
        return []

    # Look for common API patterns in script tags
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tags = soup.find_all('script')
    
    endpoints = []
    for script in script_tags:
        if script.string:
            # Look for API URLs
            api_patterns = [
                r'https?://[^"\']+\.json[^"\']*',
                r'https?://[^"\']+api[^"\']+images[^"\']*',
                r'https?://[^"\']+graphql[^"\']*'
            ]
            for pattern in api_patterns:
                matches = re.findall(pattern, script.string, re.IGNORECASE)
                endpoints.extend(matches)
    
    return list(set(endpoints))