from groq_client import GroqClient
import re

class QueryProcessor:
    def __init__(self):
        self.groq_client = GroqClient()
    
    async def decompose_query(self, user_query):
        """Decompose user query into 3-5 focused sub-queries"""
        if not user_query or len(user_query.strip()) < 3:
            raise ValueError("Query too short or empty")
        
        sub_queries = await self.groq_client.decompose_query(user_query)
        
        # Validate and clean sub-queries
        validated_queries = self._validate_sub_queries(sub_queries, user_query)
        return validated_queries[:5]  # Max 5 sub-queries
    
    def _validate_sub_queries(self, sub_queries, original_query):
        """Basic validation to ensure relevance and no duplicates"""
        if not isinstance(sub_queries, list):
            return [original_query]
        
        validated = []
        seen = set()
        
        for query in sub_queries:
            if isinstance(query, str) and query.strip():
                clean_query = re.sub(r'[^\w\s]', '', query.lower().strip())
                if clean_query not in seen and len(clean_query) > 10:
                    validated.append(query.strip())
                    seen.add(clean_query)
        
        return validated if validated else [original_query]
