from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SlideType(str, Enum):
    TITLE = "title"
    CONTENT = "content"
    IMAGE = "image"
    BULLET_POINTS = "bullet_points"
    TWO_COLUMN = "two_column"


class SlideContent(BaseModel):
    type: SlideType
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    bullet_points: Optional[List[str]] = None
    column1: Optional[str] = None
    column2: Optional[str] = None


class PresentationRequest(BaseModel):
    title: str
    author: str
    slides: List[SlideContent]
    theme: Optional[str] = "default"


class PDFPresentationRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = "Generated Presentation"
    theme: Optional[str] = "default"
    num_slides: Optional[int] = 5


class PresentationResponse(BaseModel):
    task_id: str
    status: str = "pending"


class PresentationStatus(BaseModel):
    task_id: str
    status: str
    file_url: Optional[str] = None
    message: Optional[str] = None
