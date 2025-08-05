from groq_client import GroqClient

class ContentAnalyzer:
    """Agent 3: Analyzes and synthesizes collected data"""
    
    def __init__(self):
        self.groq_client = GroqClient()

    async def analyze_content(self, collected_data, original_query):
        """Synthesize collected data into coherent analysis"""
        try:
            # Combine all content
            combined_content = self._combine_content(collected_data)

            # Ensure content fits within context limits (~4000 chars)
            if len(combined_content) > 4000:
                combined_content = combined_content[:4000]

            # Generate structured analysis
            analysis = await self.groq_client.analyze_and_structure(
                combined_content, original_query
            )

            return {
                'original_query': original_query,
                'analysis': analysis,
                'sources': self._extract_sources(collected_data),
                'total_sources': self._count_sources(collected_data),
                'word_count': len(analysis.split()) if analysis else 0
            }
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return {
                'original_query': original_query,
                'analysis': f"Analysis failed: {str(e)}",
                'sources': [],
                'total_sources': 0,
                'word_count': 0
            }

    def _combine_content(self, collected_data):
        """Combine content from all sources"""
        combined = ""
        for query, sources in collected_data.items():
            combined += f"\n--- {query} ---\n"
            for source in sources:
                if isinstance(source, dict) and 'content' in source and source['content']:
                    combined += source['content'][:500] + "\n"
        return combined

    def _extract_sources(self, collected_data):
        """Extract source URLs for citations"""
        sources = []
        for query, source_list in collected_data.items():
            for source in source_list:
                if isinstance(source, dict) and 'url' in source:
                    sources.append(source['url'])
        return list(set(sources))  # Remove duplicates
    
    def _count_sources(self, collected_data):
        """Count total number of sources"""
        count = 0
        for source_list in collected_data.values():
            count += len([s for s in source_list if isinstance(s, dict) and 'content' in s])
        return count
