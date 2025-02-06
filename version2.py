from playwright.sync_api import sync_playwright
import time
from urllib.parse import unquote
import random

def browse_web(query):
    with sync_playwright() as p:
        # Use Chromium with stealth options
        browser = p.chromium.launch(
            headless=False,  # Run in non-headless mode for debugging
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        # Create a new context with realistic user agent and viewport
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            # Disable automation flags
            bypass_csp=True,
            java_script_enabled=True,
        )
        
        page = context.new_page()

        # Navigate to Google search with proper parameters
        page.goto(f"https://www.google.com/search?q={query}&gl=us&hl=en")
        time.sleep(random.uniform(2, 5))  # Simulate human delay

        # Check if we're on a CAPTCHA page
        if page.query_selector('div#captcha'):
            print("CAPTCHA detected! Please solve it manually.")
            input("Press Enter after solving the CAPTCHA...")

        # Extract actual search result links (skip Google's tracking URLs)
        links = []
        results = page.query_selector_all('a')  # Select all anchor tags
        for result in results:
            href = result.get_attribute('href')
            if href and href.startswith('/url?q='):
                # Extract actual URL from Google's redirect
                clean_url = unquote(href.split('/url?q=')[1].split('&')[0])
                if clean_url.startswith('http'):
                    links.append(clean_url)
                    if len(links) >= 3:  # Stop after collecting 3 links
                        break

        print(f"Found {len(links)} results:")
        print(page.query_selector_all('a'))
        
        # Visit each link
        # for i, link in enumerate(links, 1):
        #     print(f"\nVisiting result {i}: {link}")
        #     try:
        #         page.goto(link, timeout=60000)
        #         page.wait_for_load_state("networkidle", timeout=60000)
                
        #         # Get content with more specific selector
        #         content = page.query_selector('body').inner_text()[:1000]
        #         print(f"\nContent preview:\n{content}\n{'-'*50}")
                
        #     except Exception as e:
        #         print(f"Error loading {link}: {str(e)}")
            
        #     time.sleep(random.uniform(2, 5))  # Add random delay between requests

        browser.close()

browse_web("latest trends in renewable energy")