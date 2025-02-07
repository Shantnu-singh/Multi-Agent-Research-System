from youtube_transcript_api import YouTubeTranscriptApi , NoTranscriptFound
import time
from playwright.async_api import async_playwright
import asyncio

def GetTranscripts(youtube_link):
  if youtube_link:
    youtube_code = youtube_link.split("v=")[1]
    open_youtube(youtube_link)
    try :
        out = YouTubeTranscriptApi.get_transcript(youtube_code)
    except NoTranscriptFound:
        transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_code)
        for transcript in transcript_list:
            out = transcript.translate('en').fetch()
            # print(out)
            # return
    except :
        return "Can't return anything as the video might not exist"
            
    main_text = ""
    for lst in out:
        if lst['text'] != "[MUSIC]":
            main_text += lst['text'] + " "
    
    return main_text

async def open_youtube(youtube_link):
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
        page = context.new_page()

        page.goto(youtube_link)
        time.sleep(2)
        browser.close