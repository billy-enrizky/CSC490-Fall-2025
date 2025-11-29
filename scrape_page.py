import logging
import requests
from bs4 import BeautifulSoup
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_page(url: str, output_dir: Path = Path("scraped_content")) -> None:
    """
    Scrape a webpage and save the content to files.
    
    Args:
        url: The URL to scrape
        output_dir: Directory to save scraped content
    """
    output_dir.mkdir(exist_ok=True)
    
    logger.info(f"Fetching content from {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching page: {e}")
        return
    
    logger.info("Parsing HTML content")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Save raw HTML
    html_file = output_dir / "page.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
    logger.info(f"Saved raw HTML to {html_file}")
    
    # Extract and save text content
    text_file = output_dir / "page.txt"
    text_content = soup.get_text(separator='\n', strip=True)
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text_content)
    logger.info(f"Saved text content to {text_file}")
    
    # Extract and save structured data (tables, links, etc.)
    structured_file = output_dir / "structured_data.txt"
    with open(structured_file, 'w', encoding='utf-8') as f:
        # Extract all links
        f.write("=== LINKS ===\n")
        for link in soup.find_all('a', href=True):
            f.write(f"{link.get_text(strip=True)}: {link['href']}\n")
        
        f.write("\n=== TABLES ===\n")
        for table in soup.find_all('table'):
            f.write("\n--- Table ---\n")
            for row in table.find_all('tr'):
                cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if cells:
                    f.write(" | ".join(cells) + "\n")
        
        f.write("\n=== HEADINGS ===\n")
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                f.write(f"{'#' * i} {heading.get_text(strip=True)}\n")
    
    logger.info(f"Saved structured data to {structured_file}")
    logger.info("Scraping completed successfully")

if __name__ == "__main__":
    url = "https://diophontine.github.io/csc490/"
    scrape_page(url)

