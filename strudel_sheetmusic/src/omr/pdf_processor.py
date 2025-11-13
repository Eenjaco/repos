"""
PDF Processing Module
Converts PDF sheet music to images for OMR processing
"""

from typing import List, Optional
from pathlib import Path
from PIL import Image
import pdf2image


class PDFProcessor:
    """
    Handles PDF to image conversion and preprocessing
    """

    def __init__(self, dpi: int = 300):
        """
        Initialize PDF processor

        Args:
            dpi: Resolution for image conversion (default: 300)
        """
        self.dpi = dpi

    def convert_to_images(
        self,
        pdf_path: str,
        page_range: Optional[tuple[int, int]] = None
    ) -> List[Image.Image]:
        """
        Convert PDF pages to images

        Args:
            pdf_path: Path to PDF file
            page_range: Optional tuple (first_page, last_page)

        Returns:
            List of PIL Image objects
        """
        try:
            images = pdf2image.convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=page_range[0] if page_range else None,
                last_page=page_range[1] if page_range else None
            )
            return images
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF: {e}")

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OMR results

        Args:
            image: Input image

        Returns:
            Preprocessed image

        TODO:
        - Implement deskewing
        - Add noise reduction
        - Enhance contrast
        - Detect and normalize staff lines
        """
        # Placeholder: Basic conversion to grayscale
        return image.convert("L")

    def save_images(
        self,
        images: List[Image.Image],
        output_dir: str,
        prefix: str = "page"
    ) -> List[Path]:
        """
        Save images to directory

        Args:
            images: List of images to save
            output_dir: Output directory path
            prefix: Filename prefix

        Returns:
            List of saved file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_paths = []
        for i, img in enumerate(images, 1):
            file_path = output_path / f"{prefix}_{i:03d}.png"
            img.save(file_path, "PNG")
            saved_paths.append(file_path)

        return saved_paths
