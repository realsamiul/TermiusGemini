#!/usr/bin/env python3
"""
Comprehensive Dengue Data Downloader for DGHS Bangladesh
Downloads all dengue status report files between 2022-2024
"""

import requests
import os
import re
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dengue_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DengueDataDownloader:
    def __init__(self, base_url="https://old.dghs.gov.bd/index.php/bd/home/5200-daily-dengue-status-report"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Create download directories
        self.download_dir = Path("dengue_reports_2022_2024")
        self.pdf_dir = self.download_dir / "pdfs"
        self.csv_dir = self.download_dir / "csvs"
        self.html_dir = self.download_dir / "htmls"
        
        for directory in [self.download_dir, self.pdf_dir, self.csv_dir, self.html_dir]:
            directory.mkdir(exist_ok=True)
    
    def get_page_content(self, url):
        """Fetch page content with error handling"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_date_from_text(self, text):
        """Extract date from Bengali/English text"""
        # Common date patterns in Bengali and English
        date_patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
            r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
            r'(\d{1,2})\s+(\d{1,2})\s+(\d{4})',  # DD MM YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    if len(match.group(1)) == 4:  # YYYY-MM-DD format
                        year, month, day = match.groups()
                    else:  # DD/MM/YYYY or DD-MM-YYYY format
                        day, month, year = match.groups()
                    
                    date_obj = datetime(int(year), int(month), int(day))
                    return date_obj
                except ValueError:
                    continue
        return None
    
    def is_date_in_range(self, date_obj, start_year=2022, end_year=2024):
        """Check if date is within the specified range"""
        if date_obj is None:
            return False
        return start_year <= date_obj.year <= end_year
    
    def extract_download_links(self, html_content):
        """Extract all download links from the page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Find all links that might contain dengue reports
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Check if it's a dengue-related link
            if any(keyword in text.lower() for keyword in ['dengue', 'ডেঙ্গু', 'press', 'প্রেস', 'release', 'রিলিজ']):
                full_url = urljoin(self.base_url, href)
                
                # Try to extract date from link text
                date_obj = self.parse_date_from_text(text)
                
                # Determine file type
                file_type = 'unknown'
                if href.lower().endswith('.pdf'):
                    file_type = 'pdf'
                elif href.lower().endswith('.csv'):
                    file_type = 'csv'
                elif href.lower().endswith('.xlsx') or href.lower().endswith('.xls'):
                    file_type = 'excel'
                elif 'html' in href.lower() or 'php' in href.lower():
                    file_type = 'html'
                
                links.append({
                    'url': full_url,
                    'text': text,
                    'date': date_obj,
                    'type': file_type
                })
        
        return links
    
    def download_file(self, url, filename, file_type):
        """Download a file with proper error handling"""
        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            
            # Determine save directory based on file type
            if file_type == 'pdf':
                save_path = self.pdf_dir / filename
            elif file_type == 'csv':
                save_path = self.csv_dir / filename
            elif file_type == 'excel':
                save_path = self.csv_dir / filename  # Save Excel files in CSV directory
            else:
                save_path = self.html_dir / filename
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded: {filename} ({len(response.content)} bytes)")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Error downloading {url}: {e}")
            return False
    
    def generate_filename(self, link_info, index):
        """Generate a proper filename for the downloaded file"""
        date_str = ""
        if link_info['date']:
            date_str = link_info['date'].strftime("%Y-%m-%d")
        else:
            date_str = f"unknown_date_{index}"
        
        # Clean the text for filename
        clean_text = re.sub(r'[^\w\s-]', '', link_info['text'])
        clean_text = re.sub(r'[-\s]+', '_', clean_text)
        
        # Determine extension
        ext = link_info['type']
        if ext == 'unknown':
            ext = 'html'  # Default to HTML for unknown types
        
        filename = f"{date_str}_{clean_text[:50]}.{ext}"
        return filename
    
    def download_all_reports(self):
        """Main method to download all dengue reports between 2022-2024"""
        logger.info("Starting comprehensive dengue data download...")
        logger.info(f"Target URL: {self.base_url}")
        
        # Get the main page
        response = self.get_page_content(self.base_url)
        if not response:
            logger.error("Failed to fetch main page")
            return False
        
        # Extract all download links
        links = self.extract_download_links(response.text)
        logger.info(f"Found {len(links)} potential download links")
        
        # Filter links by date range
        filtered_links = []
        for link in links:
            if self.is_date_in_range(link['date']):
                filtered_links.append(link)
            elif link['date'] is None:
                # Include links without clear dates for manual review
                filtered_links.append(link)
        
        logger.info(f"Filtered to {len(filtered_links)} links within 2022-2024 range")
        
        # Download each file
        successful_downloads = 0
        failed_downloads = 0
        
        for i, link in enumerate(filtered_links, 1):
            logger.info(f"Processing {i}/{len(filtered_links)}: {link['text']}")
            
            filename = self.generate_filename(link, i)
            
            if self.download_file(link['url'], filename, link['type']):
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Be respectful to the server
            time.sleep(1)
        
        # Create summary report
        self.create_summary_report(successful_downloads, failed_downloads, filtered_links)
        
        logger.info(f"Download complete! Success: {successful_downloads}, Failed: {failed_downloads}")
        return successful_downloads > 0
    
    def create_summary_report(self, successful, failed, links):
        """Create a summary report of the download process"""
        summary_path = self.download_dir / "download_summary.txt"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("DENGUE DATA DOWNLOAD SUMMARY\n")
            f.write("=" * 50 + "\n")
            f.write(f"Download Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source URL: {self.base_url}\n")
            f.write(f"Successful Downloads: {successful}\n")
            f.write(f"Failed Downloads: {failed}\n")
            f.write(f"Total Links Processed: {len(links)}\n\n")
            
            f.write("DOWNLOADED FILES:\n")
            f.write("-" * 30 + "\n")
            
            for link in links:
                date_str = link['date'].strftime('%Y-%m-%d') if link['date'] else 'Unknown Date'
                f.write(f"{date_str} - {link['text']} ({link['type']})\n")
                f.write(f"  URL: {link['url']}\n\n")
        
        logger.info(f"Summary report created: {summary_path}")

def main():
    """Main execution function"""
    print("DENGUE DATA DOWNLOADER - DGHS Bangladesh")
    print("=" * 50)
    print("Downloading all dengue status reports between 2022-2024...")
    print()
    
    downloader = DengueDataDownloader()
    
    try:
        success = downloader.download_all_reports()
        
        if success:
            print("\n✅ Download completed successfully!")
            print(f"📁 Files saved to: {downloader.download_dir}")
            print("📊 Check 'download_summary.txt' for details")
        else:
            print("\n❌ Download failed. Check the log file for details.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Download interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()

