# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Web scraping script (`scrape_page.py`) to scrape content from https://diophontine.github.io/csc490/
- Scraped content saved to `scraped_content/` directory:
  - `page.html` - Raw HTML content
  - `page.txt` - Extracted text content
  - `structured_data.txt` - Structured data including links, tables, and headings
- HTML to Jupyter notebook conversion script (`html_to_notebook.py`)
- Converted HTML content to Jupyter notebook format (`scraped_content/page.ipynb`)

