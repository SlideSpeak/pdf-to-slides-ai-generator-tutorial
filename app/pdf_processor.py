import os
import tempfile
from PyPDF2 import PdfReader
from openai import OpenAI
from typing import List, Dict, Any
from app.config import settings
from app.models import SlideContent, SlideType


class PDFProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text content from PDF bytes"""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(pdf_content)
            temp_path = temp.name

        try:
            pdf = PdfReader(temp_path)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

            return text
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def generate_presentation_content(
        self, text: str, title: str = None, num_slides: int = 5
    ) -> Dict[str, Any]:
        """Generate presentation content using OpenAI"""
        system_message = f"""
        You are an expert presentation creator. Your task is to create a well-structured presentation 
        from the provided text content. Extract the key points and organize them into a cohesive presentation.
        
        Create a presentation with the following:
        1. A title slide with an engaging title (if not provided) and subtitle
        2. {num_slides-1} content slides
        
        Structure the presentation logically and extract the most important information.
        """

        user_message = f"""
        Create a presentation based on the following content:
        
        {text[:10000]}
        
        Please structure your response in JSON format with the following structure:
        {{
            "title": "Main Title of Presentation",
            "slides": [
                {{
                    "type": "title",
                    "title": "Presentation Title",
                    "content": "Subtitle - e.g. Author's Name"
                }},
                {{
                    "type": "bullet_points",
                    "title": "Key Point 1",
                    "bullet_points": ["Point 1", "Point 2", "Point 3"]
                }},
                ...
            ]
        }}
        
        Ensure all slide content is concise and impactful. Use different slide types appropriately:
        - title: For title slides with a subtitle
        - content: For slides with paragraphs of text
        - bullet_points: For key points in a list format
        - two_column: For comparing information side by side
        """

        if title:
            user_message += f"\nUse '{title}' as the presentation title."
        response = self.client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )

        content = response.choices[0].message.content

        import json

        presentation_data = json.loads(content)

        return presentation_data
