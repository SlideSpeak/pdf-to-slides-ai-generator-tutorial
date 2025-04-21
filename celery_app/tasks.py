import os
import logging
from celery import shared_task
from app.models import PresentationRequest
from app.ppt_generator import PPTGenerator

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
