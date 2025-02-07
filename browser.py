from playwright.async_api import async_playwright
import asyncio
import time
from urllib.parse import unquote

def browse_web(query):
    with async_playwright() as p:
        # Use Chromium with stealth options
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        # Create a new context with realistic user agent and viewport
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        
        page = context.new_page()

        # Navigate to Google search with proper parameters
        # page.goto(f"https://www.bing.com/search?q={query}&gl=us&hl=en")
        page.goto(f"https://duckduckgo.com/?q={query}&ia=web&gl=us&hl=en")
        time.sleep(2)  # Simulate human delay

        # Extract actual search result links (skip Google's tracking URLs)
        links = []
        results = page.query_selector_all('a')
        for result in results:  # Get top 3 results
            href = result.get_attribute('href')
            if href and href.startswith('/url?q='):
                clean_url = unquote(href.split('/url?q=')[1].split('&')[0])
                if clean_url.startswith('http'):
                    links.append(clean_url)
                    if len(links) >= 3:  # Stop after collecting 3 links
                        break

        print(f"Found {len(links)} results:")
        # print(page.query_selector_all("li.b_algo h2 a" ))
        # print(page.inner_text())
        print(page.query_selector_all('body'))
        
        # Visit each link
        for i, link in enumerate(links, 1):
            print(f"\nVisiting result {i}: {link}")
            try:
                page.goto(link, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=60000)
                
                # Get content with more specific selector
                content = page.query_selector('body').inner_text()[:1000]
                print(f"\nContent preview:\n{content}\n{'-'*50}")
                
            except Exception as e:
                print(f"Error loading {link}: {str(e)}")
            
            time.sleep(2)  # Add delay between requests

        browser.close()

import asyncio
from playwright.async_api import async_playwright

async def view_websites(website_link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )

        # Open first page
        page = await context.new_page()
        await page.goto(website_link, timeout=60000)
        await asyncio.sleep(2)  # Simulate human delay
        
        # Open new page with modified link
        new_page_link = f"https://r.jina.ai/{website_link}"
        page2 = await context.new_page()
        await page2.goto(new_page_link, timeout=60000)
        await asyncio.sleep(2)

        # Extract all content from <body>
        body_content = await page2.evaluate("document.body.innerText")

        await browser.close()
        return body_content  # Return extracted text

async def scarpe_content(website_link):
    # make the link jina ai link
    website_link = "https://r.jina.ai/" + website_link
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        
        page = await context.new_page()
        await page.goto(website_link, timeout=60000)
        await asyncio.sleep(2)  # Simulate human delay
        await browser.close()
          
# browse_web("latest trends in renewable energy")
# view_websites()
# asyncio.run(view_websites("https://abc.com/"))

