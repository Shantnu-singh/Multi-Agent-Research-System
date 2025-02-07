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
                    - 1 YouTube video link (`youtube`)  and give me link for specific videos on that topic and make sure that video exist don't make it up.
                    Ensure the sources are reputable and trustworthy. Do not include any additional text, explanations, or formatting—only output the dictionary.  
                    Example Output:  
                    {  
                        "webpages": ["https://example1.com", "https://example2.com", "https://example3.com"],  
                        "youtube": "https://youtube.com/example_youtube_code"  
                    }  
                    the give topic is : 
            """
    return model.generate_content([promt , text] ).text
    
# print(model.generate_content("Hey How are you"))
def summerise_text(text):
    prompt = """
        1) Task: Summarize the provided content in 100 words or fewer.
        2) Focus: Retain only the most critical factual details, data, and key concepts essential for research and analysis.
        Exclude:
            - Examples, anecdotes, and stories.
            - Links, images, and any non-essential visuals.
            - Redundant or repetitive information.
            - Tangential or irrelevant details.
        3) Prioritize:
            - Core insights, trends, definitions, statistics, or findings.
            - Clarity, precision, and factual accuracy.
        4) Output: Ensure the summary is self-contained, concise, and strictly fact-based, suitable for academic or analytical purposes.
    """
    return model.generate_content([prompt , text] ).text

# text = """
# Your liver is all that and more, says Saleh Alqahtani , director of clinical liver research for Johns Hopkins Medicine. The second-largest organ in your body, your liver has some 500 critical jobs. “Your liver removes all toxins, clears medication from your body and metabolizes [breaks down] all your food,” says Dr. Alqahtani.

# It also adjust cholesterol levels, builds proteins and makes bile, which helps you absorb fats, stores sugar for when you really need it and regulates hormone levels. For your liver, that’s all in a day’s work.

# Couple prepares produce on the kitchen counter
# What could possibly go wrong?
# Your liver health may not be top of mind, but the minute it malfunctioned there wouldn’t be much else on your mind. Cirrhosis , in which liver cells are replaced with scar tissue, can prevent your liver from doing its critical jobs. So can nonalcoholic fatty liver disease , a fast-growing epidemic among the obese, which can lead to cirrhosis. “If your liver stopped working,” says Dr. Alqahtani, “toxins would accumulate, you couldn’t digest your food and medications would never leave your body.”

# In fact — you can’t live a week without your liver.

# So here’s a list of ways to avoid liver disease. Some of them are healthy behaviors you might do anyway. Others may never have occurred to you. Heed these tips to stay right with your liver.

# Be careful about alcohol consumption
# If you think only lifelong, falling-down drunks get cirrhosis of the liver — you’re mistaken. Just four ounces a day of hard liquor for men (two for women) can begin to scar your liver.

# Wash produce and steer clear of toxins
# Pesticides and other toxins can damage your liver. Read warning labels on the chemicals you use.

# Prevent hepatitis A, B and C
# Get vaccinated: Hepatitis A and B are viral diseases of the liver. While many children have now been immunized, many adults have not. Ask your doctor if you are at risk.
# Practice safe sex: Hepatitis B and C can develop into chronic conditions that may eventually destroy your liver. They are transmitted by blood and other bodily fluids.
# Wash your hands: Hepatitis A is spread through contact with contaminated food or water.
# Watch out for medications and herbs
# “The number one reason clinical [medicine] trials are stopped or drugs removed from the market is the liver,” warns Dr. Alqahtani, who adds, “20 percent of liver injury in the U.S. is caused by supplements.” The National Institutes of Health has a database of substances known to be toxic to your liver.

# Exercise and eat right
# Avoid fatty liver disease by avoiding obesity.


# Find a Doctor

# Find a Treatment Center
# Related
# Hepatitis in Children
# Endoscopic Retrograde Cholangiopancreatography (ERCP)
# Primary Sclerosing Cholangitis Treatment
# Pancreatic Neuroendocrine Tumor

# """
# print(summerise_text(text))