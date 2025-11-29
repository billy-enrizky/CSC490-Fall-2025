import logging
import json
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def html_to_markdown(html_content: str) -> str:
    """
    Convert HTML content to markdown format.
    
    Args:
        html_content: HTML string to convert
        
    Returns:
        Markdown string
    """
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.unicode_snob = True
    h.mark_code = True
    
    markdown = h.handle(html_content)
    return markdown

def create_notebook_from_html(html_file: Path, output_file: Path) -> None:
    """
    Convert HTML file to Jupyter notebook format.
    
    Args:
        html_file: Path to input HTML file
        output_file: Path to output .ipynb file
    """
    logger.info(f"Reading HTML file: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract main content from body
    body = soup.find('body')
    if not body:
        logger.error("No body tag found in HTML")
        return
    
    # Find the main content container
    main_content = body.find('div', class_='container-lg')
    if not main_content:
        main_content = body
    
    # Convert HTML to markdown
    logger.info("Converting HTML to markdown")
    markdown_content = html_to_markdown(str(main_content))
    
    # Clean up the markdown
    markdown_content = markdown_content.strip()
    
    # Create notebook structure
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": markdown_content.split('\n')
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Save notebook
    logger.info(f"Saving notebook to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    logger.info("Notebook created successfully")

if __name__ == "__main__":
    html_file = Path("scraped_content/page.html")
    output_file = Path("scraped_content/page.ipynb")
    
    create_notebook_from_html(html_file, output_file)

