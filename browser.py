from playwright.async_api import async_playwright
import asyncio
import time
import os
from urllib.parse import unquote
from gemini import summerise_text

# Serp API intergation 
from serpapi import GoogleSearch

def get_organic_results(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERP_API_KEY")
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    video_results = results.get("video_results", [])
    
    webpages = [result["link"] for result in organic_results[:3]]  # Get top 3 webpage links
    
    youtube_link = ""
    for video in video_results:
        if "youtube.com" in video["link"]:
            youtube_link = video["link"]
            break  # Take the first YouTube link available
    
    return {
        "webpages": webpages,
        "youtube": youtube_link
    }

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


async def view_websites(query , website_links):
    extracted_content = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",  
                "--disable-extensions",  
                "--disable-popup-blocking",  
                "--start-maximized"
            ]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            bypass_csp=True
        )
        page = await context.new_page()

        await page.goto(f"https://duckduckgo.com/?q={query}&ia=web&gl=us&hl=en")
        await asyncio.sleep(2)  # Simulate human delay

        for website_link in website_links:
            try:
                # First, visit the original website
                page = await context.new_page()
                await page.goto(website_link, timeout=60000)
                await asyncio.sleep(2)  # Simulate human delay

                # Visit the transformed link (Jina AI)
                new_page_link = f"https://r.jina.ai/{website_link}"
                page2 = await context.new_page()
                await page2.goto(new_page_link, timeout=60000)
                await asyncio.sleep(2)

                # Extract <body> text
                body_content = await page2.evaluate("document.body.innerText")
                extracted_content[website_link] = summerise_text(body_content)

                await page.close()
                await page2.close()
                
            except Exception as e:
                extracted_content[website_link] = f"Error fetching content: {e}"

        await browser.close()

    return extracted_content

# print(asyncio.run(view_websites("what is artificial intelligence" , ["https://abc.com/" , "https://www.ibm.com/think/topics/artificial-intelligence"])))
