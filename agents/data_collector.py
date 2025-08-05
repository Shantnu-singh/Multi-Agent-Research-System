import asyncio
import os
import logging
from datetime import datetime
from playwright.async_api import async_playwright
from serpapi import GoogleSearch

logger = logging.getLogger(__name__)

class DataCollector:
    """Agent 2: Collects data from web sources"""
    
    def __init__(self):
        self.max_sources_per_query = 3
        self.serp_api_key = os.getenv("SERP_API_KEY")
    
    async def collect_data(self, sub_queries):
        """Collect data for each sub-query from 2-3 sources"""
        all_data = {}
        
        for query in sub_queries:
            try:
                print(f"Collecting data for: {query}")
                sources = await self._search_sources(query)
                query_data = await self._scrape_sources(sources[:3])
                all_data[query] = query_data
                await asyncio.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"Error collecting data for '{query}': {e}")
                all_data[query] = []
        
        return all_data
    
    async def _search_sources(self, query):
        """Get search results for a query"""
        urls = []
        
        try:
            if self.serp_api_key:
                # Use SERP API
                urls = self._get_serp_results(query)
            else:
                # Fallback to DuckDuckGo scraping
                urls = await self._scrape_duckduckgo(query)
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
        
        return urls
    
    def _get_serp_results(self, query):
        """Get search results using SERP API"""
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.serp_api_key
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results.get("organic_results", [])
            return [result["link"] for result in organic_results[:3]]
        except Exception as e:
            print(f"SERP API error: {e}")
            return []
    
    async def _scrape_duckduckgo(self, query):
        """Fallback: scrape DuckDuckGo for URLs"""
        urls = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = await context.new_page()
                await page.goto(f"https://duckduckgo.com/?q={query}")
                await asyncio.sleep(2)
                
                # Extract result links
                links = await page.query_selector_all('a[href*="http"]')
                for link in links[:5]:
                    href = await link.get_attribute('href')
                    if href and href.startswith('http') and 'duckduckgo.com' not in href:
                        urls.append(href)
                        if len(urls) >= 3:
                            break
                
                await browser.close()
        except Exception as e:
            print(f"DuckDuckGo scraping error: {e}")
        
        return urls
    
    async def _scrape_sources(self, urls):
        """Scrape content from URLs"""
        scraped_data = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            for url in urls:
                try:
                    # Try Jina AI first
                    content = await self._extract_with_jina(context, url)
                    
                    if not content:
                        # Fallback to direct scraping
                        content = await self._extract_direct(context, url)
                    
                    if content and len(content) > 100:
                        scraped_data.append({
                            'url': url,
                            'content': content[:1000],
                            'word_count': len(content.split()),
                            'scraped_at': datetime.now().isoformat()
                        })
                
                except Exception as e:
                    print(f"Failed to scrape {url}: {e}")
                    scraped_data.append({'url': url, 'content': '', 'error': str(e)})
                
                await asyncio.sleep(1)
            
            await browser.close()
        
        return scraped_data
    
    async def _extract_with_jina(self, context, url):
        """Extract content using Jina AI"""
        try:
            jina_url = f"https://r.jina.ai/{url}"
            page = await context.new_page()
            await page.goto(jina_url, timeout=30000)
            content = await page.evaluate("document.body.innerText")
            await page.close()
            return content
        except:
            return None
    
    async def _extract_direct(self, context, url):
        """Direct content extraction fallback"""
        try:
            page = await context.new_page()
            await page.goto(url, timeout=30000)
            
            # Remove unwanted elements
            await page.evaluate("""
                const unwanted = document.querySelectorAll('script, style, nav, footer, aside');
                unwanted.forEach(el => el.remove());
            """)
            
            content = await page.evaluate("document.body.innerText")
            await page.close()
            return content
        except:
            return None
