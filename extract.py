import re
import argparse
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

# Define multiple regex patterns for OAuth URL parameters
oauth_patterns = [
    re.compile(
        r"(https?://[^\s]+?)(\?|&)(client_id|redirect_uri|response_type|scope|state)=[^\s&]+",
        re.IGNORECASE,
    ),
    re.compile(
        r"(https?://[^\s]+?)(\?|&)(access_token|authorization_code|token_type|code_challenge)=[^\s&]+",
        re.IGNORECASE,
    ),
]


def extract_oauth_urls(url):
    """Check if a URL contains OAuth parameters."""
    for pattern in oauth_patterns:
        match = pattern.search(url)
        if match:
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            if any(
                param in params
                for param in [
                    "client_id",
                    "redirect_uri",
                    "response_type",
                    "scope",
                    "state",
                    "access_token",
                    "authorization_code",
                    "token_type",
                    "code_challenge",
                ]
            ):
                print(f"Potential OAuth URL found: {url}")
                return url
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Extract OAuth URLs from a domain or file."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=argparse.FileType("r"),
        help="File with URLs to scan or '-' for stdin.",
        required=True,
    )

    args = parser.parse_args()

    try:
        urls = [line.strip() for line in args.file if line.strip()]
        print("Loaded URLs:", urls)  # Debugging output
        for url in urls:
            # Debugging output to verify each URL being processed
            print(f"Processing URL: {url}")
            extract_oauth_urls(url)
    except Exception as e:
        print("Error reading file:", e)


if __name__ == "__main__":
    main()
