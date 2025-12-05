# """
# PDF Generation Service using WeasyPrint
# """
# from weasyprint import HTML, CSS
# from io import BytesIO
# import logging

# logger = logging.getLogger(__name__)

# class PDFGenerator:
#     """Handles PDF generation from HTML content"""
    
#     def __init__(self):
#         """Initialize PDF generator"""
#         self.default_css = CSS(string='''
#             @page {
#                 size: A4;
#                 margin: 2cm;
#             }
#         ''')
    
#     def generate(self, html_content: str, custom_css: str = None) -> bytes:
#         """
#         Generate PDF from HTML content
        
#         Args:
#             html_content: HTML string to convert to PDF
#             custom_css: Optional custom CSS string
            
#         Returns:
#             PDF content as bytes
            
#         Raises:
#             Exception: If PDF generation fails
#         """
#         try:
#             logger.info("Starting PDF generation")
            
#             # Create HTML object
#             html = HTML(string=html_content)
            
#             # Prepare CSS
#             stylesheets = [self.default_css]
#             if custom_css:
#                 stylesheets.append(CSS(string=custom_css))
            
#             # Generate PDF
#             pdf_bytes = html.write_pdf(stylesheets=stylesheets)
            
#             logger.info("PDF generated successfully")
#             return pdf_bytes
            
#         except Exception as e:
#             logger.error(f"Failed to generate PDF: {str(e)}")
#             raise Exception(f"PDF generation failed: {str(e)}")
    
#     def generate_from_file(self, html_file_path: str) -> bytes:
#         """
#         Generate PDF from HTML file
        
#         Args:
#             html_file_path: Path to HTML file
            
#         Returns:
#             PDF content as bytes
#         """
#         try:
#             html = HTML(filename=html_file_path)
#             pdf_bytes = html.write_pdf(stylesheets=[self.default_css])
#             return pdf_bytes
#         except Exception as e:
#             logger.error(f"Failed to generate PDF from file: {str(e)}")
#             raise Exception(f"PDF generation from file failed: {str(e)}")


from xhtml2pdf import pisa
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    
    
    def __init__(self):
        
        pass
    
    def generate(self, html_content: str, custom_css: str = None) -> bytes:
        
        try:
            logger.info("Starting PDF generation")
            
            # Combine HTML with CSS if provided
            if custom_css:
                html_with_css = f"<style>{custom_css}</style>{html_content}"
            else:
                html_with_css = html_content
            
            # Add default styling
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm;
                    }}
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                </style>
            </head>
            <body>
                {html_with_css}
            </body>
            </html>
            """
            
            # Create a BytesIO buffer
            pdf_buffer = BytesIO()
            
            # Generate PDF
            pisa_status = pisa.CreatePDF(
                full_html,
                dest=pdf_buffer
            )
            
            if pisa_status.err:
                raise Exception("PDF generation had errors")
            
            # Get PDF bytes
            pdf_bytes = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            logger.info("PDF generated successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Failed to generate PDF: {str(e)}")
            raise Exception(f"PDF generation failed: {str(e)}")
    
    # def generate_from_file(self, html_file_path: str) -> bytes:
    #     """
    #     Generate PDF from HTML file
        
    #     Args:
    #         html_file_path: Path to HTML file
            
    #     Returns:
    #         PDF content as bytes
    #     """
    #     try:
    #         with open(html_file_path, 'r', encoding='utf-8') as f:
    #             html_content = f.read()
    #         return self.generate(html_content)
    #     except Exception as e:
    #         logger.error(f"Failed to generate PDF from file: {str(e)}")
    #         raise Exception(f"PDF generation from file failed: {str(e)}")