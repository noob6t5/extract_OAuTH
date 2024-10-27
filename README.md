# OAuth URL Extractor

![oauth](https://github.com/user-attachments/assets/1999f30e-1941-4ea4-860f-fd3bf732239a)

 `extract_oauth ` is a CLI  tool to  scan a list of URLs from a file and identify potential OAuth URLs based on common OAuth parameters. This tool supports input from a file and can handle URLs in various formats. It helps bug hunter's, red teamer's as well developer's to quickly jump to Oauth based url and find bug's..

## Features
- Extract URLs containing OAuth-related parameters (`client_id`, `redirect_uri`, `response_type`, etc.).
- Display a summary of the total URLs processed and the number of OAuth URLs found.
- Save extracted OAuth URLs to a specified output file.
- Supports input from both a file and stdin for versatile usage.

# Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/extract_oauth_urls.git
cd extract_oauth_urls
```
# Usuage

python3 extract.py -f /path/to/your/urls.txt

python3 extract.py -f /path/to/your/urls.txt -o custom_output.txt

cat /path/to/your/urls.txt | python3 extract.py -f -

![oauth output](https://github.com/user-attachments/assets/ade78908-25f0-4539-a078-3ba4567c4d26)




