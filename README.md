Automated WhatsApp Web Chat Monitor
This repository contains a fully automated Python script that sets up WhatsApp Web, monitors a user-specified chat for LinkedIn URLs, and saves them to a file.

Features
Fully Automated Setup:

Installs required Python modules automatically.
Uses webdriver-manager to download the correct ChromeDriver.
Automatically creates a persistent Chrome profile folder so that the QR code needs to be scanned only once.
Persistent Session:

On the first run, you scan the QR code.
On subsequent runs, the saved session is reused, bypassing the QR scan.
Chat Search & Monitoring:

Prompts you for a chat keyword (case-insensitive) instead of a hardcoded group name.
Automatically searches for and opens the chat that matches the keyword.
Monitors the chat for LinkedIn URLs and saves them to linkedin_urls.txt.
Requirements
Python 3.x
Internet connection
How It Works
Automatic Setup:
The script checks for and installs missing dependencies (Selenium and webdriver-manager), downloads the appropriate ChromeDriver, and creates a persistent profile folder.

First Run:
When you run the script for the first time, it opens WhatsApp Web and prompts you to scan the QR code. The session data (cookies, cache, etc.) is saved in the profile folder.

Subsequent Runs:
The saved session is loaded automatically, so you won't need to scan the QR code again.

Chat Search & Monitoring:
You enter a keyword for the chat to search (e.g., "data"). The script finds and opens the chat whose title contains the keyword (case-insensitive) and continuously monitors the chat for any LinkedIn URLs, which are then saved to linkedin_urls.txt.

Usage
Clone the Repository:


gi
Run the Script:

python whatsapp_url_extractor.py



Follow On-Screen Instructions:

On the first run, scan the QR code using WhatsApp on your phone.
When prompted, enter the keyword for the chat you want to monitor.
The script will then monitor the chat and save any LinkedIn URLs found to linkedin_urls.txt.
License
This project is licensed under the MIT License.
