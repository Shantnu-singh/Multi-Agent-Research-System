import asyncio
from playwright.async_api import async_playwright
from gemini import summerise_text

async def view_websites(website_links):
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

print(asyncio.run(view_websites(["https://abc.com/" , "https://www.ibm.com/think/topics/artificial-intelligence"])))
