import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import ast

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
model2 = genai.GenerativeModel("gemini-pro")


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

def generate_final_report(text):
    prompt = """
        1) Title: A clear, concise, and professional title summarizing the topic.
        2) Introduction: A brief overview of the topic, why it matters, and its relevance in the current landscape.
            Recent Developments:
            - Summarize the latest advancements, breakthroughs, or trends related to the topic.
            - Include references to key sources and expert statements.
        3) Key Statistics:
            - present relevant numerical data, percentages, charts, or trends in a well-organized manner.
            - Provide comparisons, growth rates, and patterns observed.
        4) Expert Opinions & Analysis:
            - Curate insights from subject matter experts, researchers, or industry leaders.
            - Highlight different viewpoints and provide a critical analysis.
        5) Challenges & Future Outlook:
            - Discuss any barriers, controversies, or limitations associated with the topic.
            - Predict potential future developments based on current trends.
        6) Conclusion:
            - Provide a summary of the findings, emphasizing key takeaways.
            - Include a personal perspective or recommendations based on the analyzed data.
        7) References:
            - List all sources in markdown format with proper links.
        8) Ensure that the output follows strict markdown syntax for readability, using:
            - # for headings,
            - ## for subheadings,
            - for bullet points,
            - **bold** for emphasis,
            - > blockquotes for expert statements,
            - `code` for inline important details.
    """
    return model2.generate_content([prompt , text] ).text
