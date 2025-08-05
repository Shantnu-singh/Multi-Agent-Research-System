import asyncio
import sys
import logging
from datetime import datetime
from agents.query_processor import QueryProcessor
from agents.data_collector import DataCollector
from agents.content_analyzer import ContentAnalyzer
from agents.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResearchSystem:
    """Main research system orchestrating all agents"""
    
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.data_collector = DataCollector()
        self.content_analyzer = ContentAnalyzer()
        self.report_generator = ReportGenerator()

    async def process_query(self, user_query):
        """Main pipeline to process user query and generate PDF report"""
        try:
            print(f" Starting research for: '{user_query}'")
            
            # Agent 1: Process query into sub-queries
            print(" Agent 1: Processing query...")
            sub_queries = await self.query_processor.decompose_query(user_query)
            print(f"Generated {len(sub_queries)} sub-queries: {sub_queries}")

            # Agent 2: Collect data for each sub-query
            print(" Agent 2: Collecting data...")
            collected_data = await self.data_collector.collect_data(sub_queries)
            total_sources = sum(len(data) for data in collected_data.values())
            print(f"Collected data from {total_sources} sources")

            # Agent 3: Analyze and synthesize content
            print(" Agent 3: Analyzing content...")
            analyzed_content = await self.content_analyzer.analyze_content(
                collected_data, user_query
            )

            # Agent 4: Generate PDF report
            print(" Agent 4: Generating PDF report...")
            pdf_path = await self.report_generator.generate_report(
                analyzed_content, user_query
            )

            return pdf_path

        except Exception as e:
            print(f" Error in research system: {e}")
            return None

async def main():
    """Main entry point"""
    print(" Multi-Agent Research System")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        query = input("Enter your research query: ").strip()
    else:
        query = " ".join(sys.argv[1:])
    
    if not query:
        print(" Please provide a research query")
        return

    system = ResearchSystem()
    pdf_path = await system.process_query(query)

    if pdf_path:
        print(f"\nReport generated successfully: {pdf_path}")
        print(f" Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("\n Failed to generate report")

if __name__ == "__main__":
    asyncio.run(main())
