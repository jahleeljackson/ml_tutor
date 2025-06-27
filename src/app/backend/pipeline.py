
from scraper import scrape_text
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chatbot.vectorstore import VectorStore
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

DISTILL_URL = "https://distill.pub/" 
GRADIENT_URL = "https://thegradient.pub/"
VECTORESTORE_FILE_PATH = "app/chatbot/vectorstore_dir"

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
    
def get_text():
    '''Fetches the latest articles from Distill and The Gradient, scrapes their text content, and combines them into a single Document object.'''
    distill_dict = scrape_text(DISTILL_URL, max_pages=5)
    distill_text = ""
    for key in distill_dict.keys():
        distill_text += distill_dict[key] + "\n\n"

    gradient_dict = scrape_text(GRADIENT_URL, max_pages=5) 
    gradient_text = ""
    for key in gradient_dict.keys():
        gradient_text += gradient_dict[key] + "\n\n"
    # Combine the texts from both sources
    new_content = distill_text + gradient_text
    new_document = Document(page_content=new_content, metadata={"source": "distill_and_gradient"})
    print(f"New content length: {len(new_content)} characters.")
    return new_document

def splitter(document: Document) -> list[Document]:
    """Splits the text into manageable chunks."""
    # Define the text splitter to split the documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        add_start_index=True,
    )
    # Split the text into chunks
    chunks = text_splitter.split_documents([document])
    if not chunks:
        raise ValueError("No chunks were created from the document.")
    else:
        print(f"Split document into {len(chunks)} chunks.")
    return chunks

def main():
    '''Main function to run the web scraping pipeline, which fetches new content, splits it into chunks, and updates the vector store.'''
    # Load the existing vector store
    vectorstore = VectorStore(file_path=VECTORESTORE_FILE_PATH)
    # Get new content from the websites
    new_content = get_text()
    # Split the new content into manageable chunks
    new_chunks = splitter(new_content)
    # Update the vector store with the new chunks
    vectorstore.update_vectorstore(new_chunks)
