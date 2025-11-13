"""
OMR (Optical Music Recognition) Module
Handles PDF processing and music notation recognition
"""

from .pdf_processor import PDFProcessor
from .omr_engine import OMREngine

__all__ = ["PDFProcessor", "OMREngine"]
