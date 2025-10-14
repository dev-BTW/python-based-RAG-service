# crawler.py

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import trafilatura

class Crawler:
    def __init__(self, start_url, max_pages=30, crawl_delay_ms=500):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.crawl_delay = crawl_delay_ms / 1000.0
        self.robot_parser = self._get_robot_parser(start_url)
        self.visited_urls = set()
        self.pages = []

    def _get_robot_parser(self, url):
        robots_url = urljoin(url, "/robots.txt")
        parser = RobotFileParser()
        try:
            parser.set_url(robots_url)
            parser.read()
        except Exception as e:
            print(f"Could not fetch or parse robots.txt: {e}")
        return parser

    def _is_valid_url(self, url):
        parsed_url = urlparse(url)
        return (
            parsed_url.netloc == self.domain and
            url not in self.visited_urls and
            self.robot_parser.can_fetch("*", url) and
            parsed_url.scheme in ["http", "httpshttps"]
        )

    def _extract_text_and_links(self, html_content, page_url):
        # Use trafilatura for main content extraction
        text = trafilatura.extract(html_content, include_comments=False, include_tables=False)
        
        # Use BeautifulSoup to find all the links on the page
        soup = BeautifulSoup(html_content, 'html.parser')
        links = {urljoin(page_url, a['href']) for a in soup.find_all('a', href=True)}
        
        return text or "", links # Ensure text is not None

    def crawl(self):
        urls_to_visit = [self.start_url]
        
        while urls_to_visit and len(self.pages) < self.max_pages:
            current_url = urls_to_visit.pop(0)
            
            if not self._is_valid_url(current_url):
                continue
                
            print(f"Crawling: {current_url}")
            self.visited_urls.add(current_url)
            
            try:
                time.sleep(self.crawl_delay)
                # **MODIFICATION HERE: Using a complete and standard User-Agent**
                response = requests.get(
                    current_url, 
                    timeout=5, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}
                )
                response.raise_for_status()

                if 'text/html' not in response.headers.get('Content-Type', ''):
                    continue

                text, new_links = self._extract_text_and_links(response.text, current_url)
                
                if text:
                    self.pages.append({'url': current_url, 'text': text})

                for link in new_links:
                    if self._is_valid_url(link):
                        urls_to_visit.append(link)

            except requests.RequestException as e:
                print(f"Error crawling {current_url}: {e}")

        return self.pages