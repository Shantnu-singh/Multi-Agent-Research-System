from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        ))
    
    async def generate_report(self, analyzed_content, original_query):
        """Generate professional PDF report"""
        try:
            # Create output directory
            os.makedirs('sample_outputs', exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sample_outputs/research_report_{timestamp}.pdf"
            
            # Create PDF
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            
            # Title Page
            story.append(Paragraph(f"Research Report: {original_query}", 
                                 self.styles['CustomTitle']))
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", 
                                 self.styles['Normal']))
            story.append(Spacer(1, 0.5*inch))
            
            # Content
            analysis_text = analyzed_content.get('analysis', '')
            
            # Split analysis into paragraphs and add to story
            paragraphs = analysis_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), self.styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
            
            # Add sources if available
            sources = analyzed_content.get('sources', [])
            if sources:
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph("Sources:", self.styles['Heading2']))
                for i, source in enumerate(sources[:5], 1):  # Max 5 sources
                    story.append(Paragraph(f"{i}. {source}", self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            # Quality check
            if self._quality_check(filename, analyzed_content):
                return filename
            else:
                raise Exception("Quality check failed")
                
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def _quality_check(self, filename, content):
        """Basic quality check for generated report"""
        try:
            # Check if file exists and has content
            if not os.path.exists(filename) or os.path.getsize(filename) < 1000:
                return False
            
            # Check if analysis has minimum content
            analysis = content.get('analysis', '')
            if len(analysis.split()) < 50:  # Minimum 50 words
                return False
            
            return True
        except:
            return False
