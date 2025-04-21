import os
import logging
from celery import shared_task
from app.models import PresentationRequest, PDFPresentationRequest
from app.ppt_generator import PPTGenerator
from app.pdf_processor import PDFProcessor

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_presentation_task(self, request_dict):
    """Generate a PowerPoint presentation asynchronously"""
    try:
        request = PresentationRequest(**request_dict)

        logger.info(f"Starting presentation generation for: {request.title}")

        generator = PPTGenerator()
        file_path = generator.generate_presentation(request)

        file_url = f"/download/{os.path.basename(file_path)}"

        return {
            "status": "completed",
            "file_url": file_url,
            "message": "Presentation generated successfully",
        }

    except Exception as e:
        logger.error(f"Error generating presentation: {str(e)}")
        self.update_state(
            state="FAILURE", meta={"status": "failed", "message": f"Error: {str(e)}"}
        )
        raise


@shared_task(bind=True)
def generate_presentation_from_pdf_task(self, pdf_text, request_dict):
    """Generate a PowerPoint presentation from PDF text asynchronously"""
    try:
        request = PDFPresentationRequest(**request_dict)

        logger.info(f"Starting presentation generation from PDF")

        processor = PDFProcessor()
        presentation_data = processor.generate_presentation_content(
            pdf_text, title=request.title, num_slides=request.num_slides
        )

        presentation_request = PresentationRequest(
            title=presentation_data.get(
                "title", request.title or "Generated Presentation"
            ),
            author=request.author,
            theme=request.theme,
            slides=presentation_data.get("slides", []),
        )

        generator = PPTGenerator()
        file_path = generator.generate_presentation(presentation_request)

        file_url = f"/download/{os.path.basename(file_path)}"

        return {
            "status": "completed",
            "file_url": file_url,
            "message": "Presentation generated successfully from PDF",
        }

    except Exception as e:
        logger.error(f"Error generating presentation from PDF: {str(e)}")
        self.update_state(
            state="FAILURE", meta={"status": "failed", "message": f"Error: {str(e)}"}
        )
        raise
