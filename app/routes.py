from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.schemas import PDFRequest
from app.services.template_renderer import TemplateRenderer
from app.services.pdf_generator import PDFGenerator
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

template_renderer = TemplateRenderer()
pdf_generator = PDFGenerator()

@router.post("/generate-pdf", response_class=Response)
async def generate_pdf(request: PDFRequest):
    
    try:
        logger.info(f"Generating PDF for title: {request.title}")
        
        # Render HTML from template
        html_content = template_renderer.render(
            template_name="price_list.html",
            context=request.dict()
        )
        
        # Generate PDF from HTML
        pdf_bytes = pdf_generator.generate(html_content)
        
        # Return PDF as downloadable file
        filename = f"{request.title.replace(' ', '_').lower()}_{request.date}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )
