import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import ast

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def give_relevant_link(text):
    promt = """You are an advanced AI system. Your task is to return only a Python dictionary containing the most reliable, up-to-date, and relevant links for a given topic.  
                    For any input topic, return a dictionary with exactly: 
                    - don't write anything including "json" in the result .
                    - The top 3 webpage links (`webpages`)  
                    - 1 YouTube video link (`youtube`)  
                    Ensure the sources are reputable and trustworthy. Do not include any additional text, explanations, or formatting—only output the dictionary.  
                    Example Output:  
                    {  
                        "webpages": ["https://example1.com", "https://example2.com", "https://example3.com"],  
                        "youtube": "https://youtube.com/example"  
                    }  
                    the give topic is : 
            """
    return model.generate_content([promt , text] ).text
    
# print(model.generate_content("Hey How are you"))
