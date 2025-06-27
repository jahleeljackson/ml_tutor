import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_all_links(url):
    """Fetch all links from a given URL"""
    try:
        # Send HTTP request
        headers = {'User-Agent': 'Mozilla/5.0'}  # Some sites require user-agent
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all links
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            if href and not href.startswith(('javascript:', 'mailto:', 'tel:')):
                # Convert relative URLs to absolute
                absolute_url = urljoin(url, href)
                # Clean URL by removing fragments (#) and query parameters (?)
                parsed = urlparse(absolute_url)
                clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                links.add(clean_url)
        
        return links
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()
    
def get_text_from_url(url):
    """Fetch and return the text content from a URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        all_text = soup.get_text(separator=' ', strip=True)

        return all_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def scrape_text(starter_url, max_pages=10):
    """Scrape text content from distill.pub & thegredient.pub starting from a given URL."""
    site_texts = {}
    pages = 0
    for url in get_all_links(starter_url):
        if pages >= max_pages:
            break

        if url[:22] == "https://distill.pub/20":
            try:
                text = get_text_from_url(url)
                site_texts[url] = text
            except Exception as e:    
                print(f"Error processing {url}: {e}")
            pages += 1
        if url[:23] == "https://thegradient.pub":
            try:
                text = get_text_from_url(url)
                site_texts[url] = text
            except Exception as e:    
                print(f"Error processing {url}: {e}")
            pages += 1
    return site_texts
    
# Example usage
if __name__ == "__main__":
    print(scrape_text("https://distill.pub/", max_pages=5).keys())