import sys
import re
import argparse
import requests
from urllib.parse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup

# regex patterns for OAuth URL parameters
oauth_patterns = [
    re.compile(r'(https?://[^\s]+?)(\?|&)(client_id|redirect_uri|response_type|scope|state)=[^\s&]+', re.IGNORECASE),
    re.compile(r'(https?://[^\s]+?)(\?|&)(access_token|authorization_code|token_type|code_challenge)=[^\s&]+', re.IGNORECASE),
]

def extract_oauth_urls(url):
    """Check if a URL contains OAuth parameters."""
    for pattern in oauth_patterns:
        match = pattern.search(url)
        if match:
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            if any(param in params for param in ["client_id", "redirect_uri", "response_type", "scope", "state", "access_token", "authorization_code", "token_type", "code_challenge"]):
                print(f"Potential OAuth URL found: {url}")
                return url
    return None

def crawl_and_extract_oauth(domain):
    """Crawl a domain to find OAuth URLs."""
    visited = set()
    to_visit = [domain]
    oauth_urls = []

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract and print OAuth URLs from the current page
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if extract_oauth_urls(full_url):
                    oauth_urls.append(full_url)
                
                # If it's a link within the same domain, add it to the queue
                if urlparse(full_url).netloc == urlparse(domain).netloc and full_url not in visited:
                    to_visit.append(full_url)
        except requests.RequestException:
            continue

    return oauth_urls

def main():
    parser = argparse.ArgumentParser(description="Extract OAuth URLs from a domain, file, or stdin.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", type=str, help="Domain to scan for OAuth URLs.")
    group.add_argument("-f", "--file", type=argparse.FileType("r"), help="File with URLs to scan or '-' for stdin.")
    
    args = parser.parse_args()

    if args.domain:
        print(f"Scanning domain: {args.domain}")
        oauth_urls = crawl_and_extract_oauth(args.domain)
        print(f"Found OAuth URLs: {oauth_urls}")
    elif args.file:
        # Read URLs from the file or stdin and scan for OAuth URLs
        urls = [line.strip() for line in args.file if line.strip()]
        for url in urls:
            extract_oauth_urls(url)

if __name__ == "__main__":
    main()
