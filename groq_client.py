import os
import time
import random
import ast
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    """Groq API client with retry logic and error handling"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        # Updated to use a currently supported model
        self.model = "llama3-8b-8192"  # Fast and reliable alternative
        # Alternative options: "llama3-70b-8192", "gemma-7b-it"
    
    async def generate_with_retry(self, prompt, max_retries=3, max_tokens=1000):
        """Generate content with retry logic for rate limits"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
            except Exception as e:
                error_str = str(e).lower()
                if ("rate_limit" in error_str or "too many requests" in error_str) and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited, waiting {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    raise e
    
    async def decompose_query(self, query):
        """Decompose query into focused sub-queries"""
        prompt = f"""
        Decompose the following research query into 3-5 focused sub-queries that would help gather comprehensive information.
        
        Rules:
        - Each sub-query should be specific and searchable
        - Sub-queries should cover different aspects of the main topic
        - Return ONLY a Python list of strings, no other text
        - Each sub-query should be 3-8 words long
        
        Query: "{query}"
        
        Example format: ["specific aspect 1", "specific aspect 2", "specific aspect 3"]
        """
        
        response = await self.generate_with_retry(prompt, max_tokens=200)
        
        try:
            # Clean the response and parse as Python list
            cleaned = response.strip()
            
            # Remove code block markers if present
            if cleaned.startswith('```'):
                lines = cleaned.split('\n')
                for i, line in enumerate(lines):
                    if '[' in line:
                        cleaned = line
                        break
            
            # Try to extract list from response
            if '[' in cleaned and ']' in cleaned:
                start = cleaned.find('[')
                end = cleaned.rfind(']') + 1
                cleaned = cleaned[start:end]
            
            sub_queries = ast.literal_eval(cleaned)
            return sub_queries if isinstance(sub_queries, list) else [query]
            
        except Exception as e:
            print(f"Failed to parse sub-queries: {e}")
            # Fallback: create basic sub-queries
            return [
                f"{query} overview",
                f"{query} benefits applications", 
                f"{query} challenges issues",
                f"{query} future trends"
            ]
    
    async def summarize_content(self, content, max_chars=4000):
        """Summarize content focusing on key facts"""
        if len(content) > max_chars:
            content = content[:max_chars] + "..."
        
        prompt = f"""
        Summarize the following content in 100-150 words, focusing on key facts and insights:
        
        Content: {content}
        
        Requirements:
        - Extract only the most important factual information
        - Focus on data, statistics, key findings
        - Remove examples and anecdotes
        - Keep it concise and fact-based
        """
        
        return await self.generate_with_retry(prompt, max_tokens=300)
    
    async def analyze_and_structure(self, collected_data, original_query):
        """Analyze collected data and create structured report content"""
        prompt = f"""
        Analyze the following research data and create a structured analysis for the query: "{original_query}"
        
        Data: {collected_data}
        
        Create a structured response with exactly these sections:
        
        ## Introduction
        Brief overview of the topic and its significance
        
        ## Key Findings
        3-4 main points with supporting facts and data
        
        ## Analysis and Insights
        Deeper analysis of trends, patterns, and implications
        
        ## Conclusion
        Summary of key takeaways and future outlook
        
        Requirements:
        - Keep total response under 400 words
        - Focus on factual information
        - Include specific data points when available
        - Use clear, professional language
        """
        
        return await self.generate_with_retry(prompt, max_tokens=800)
