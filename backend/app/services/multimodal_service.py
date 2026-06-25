import time
import tempfile
import os
from functools import lru_cache
from typing import Any, Optional
from fastapi import HTTPException, status

from PIL import Image, ImageOps
import asyncio
import numpy as np

from app.core.config import get_settings
from app.services.ollama_client import OllamaClient


class MultimodalService:
    _whisper_model: Optional[Any] = None
    _latex_ocr_model: Optional[Any] = None

    def __init__(self):
        self.settings = get_settings()
        self.ollama_client = OllamaClient()

    def _get_whisper_model(self) -> Any:
        if self._whisper_model is None:
            from faster_whisper import WhisperModel

            # Force CPU usage and int8 for optimization as requested
            device = "cpu"
            compute_type = "int8"
            self._whisper_model = WhisperModel(
                self.settings.whisper_model_size, 
                device=device, 
                compute_type=compute_type
            )
        return self._whisper_model

    def _get_latex_ocr_model(self):
        if self._latex_ocr_model is None:
            os.environ.setdefault("NO_ALBUMENTATIONS_UPDATE", "1")

            try:
                from pix2tex.cli import LatexOCR
            except ImportError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                    detail="pix2tex (LatexOCR) is not installed or available."
                )

            try:
                # Load the model
                model = LatexOCR()
                
                # Attempt to force the underlying model to CPU if it's accessible
                if hasattr(model, 'model') and hasattr(model.model, 'to'):
                    model.model.to('cpu')
                    
                self._latex_ocr_model = model
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to load the Vision model (LatexOCR) for image processing: {str(e)}"
                )
        return self._latex_ocr_model

    def _normalize_content(self, text: str) -> str:
        import re
        
        # Asegurarse de que NO existan backticks de Markdown (```)
        content = re.sub(r'```(?:latex|tex)?', '', text, flags=re.IGNORECASE)
        content = content.replace('```', '')
        
        # Reemplazar guiones largos por normales
        content = content.replace('—', '-').replace('–', '-')
        
        # Eliminar caracteres de "ruido" de OCR (ej. interrogaciones ? huérfanas)
        content = content.replace('?', '')
        # Eliminar pipes huérfanos al final de palabras o espacios
        content = re.sub(r'([a-zA-Z0-9_])\|(?=\s|$)', r'\1', content)
        
        # Detectar y eliminar patrones de conteo iniciales en audio (como "1, 2, 3, 4")
        content = content.strip()
        content = re.sub(r'^(?:\d+[\s,]+){2,}', '', content)
        
        return content.strip()

    def _otsu_threshold(self, gray: np.ndarray) -> np.ndarray:
        histogram = np.bincount(gray.ravel(), minlength=256).astype(float)
        total = gray.size
        pixel_sum = np.dot(np.arange(256), histogram)

        weight_background = np.cumsum(histogram)
        weight_foreground = total - weight_background

        sum_background = np.cumsum(np.arange(256) * histogram)
        sum_foreground = pixel_sum - sum_background

        valid = (weight_background > 0) & (weight_foreground > 0)
        variance = np.zeros(256, dtype=float)
        variance[valid] = (
            (sum_background[valid] / weight_background[valid])
            - (sum_foreground[valid] / weight_foreground[valid])
        ) ** 2 * weight_background[valid] * weight_foreground[valid]

        threshold = int(np.argmax(variance))
        return np.where(gray > threshold, 255, 0).astype(np.uint8)

    async def process_audio(self, file_content: bytes, filename: str) -> tuple[str, str, float]:
        start_time = time.time()
        
        # Save audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_audio:
            temp_audio.write(file_content)
            temp_audio_path = temp_audio.name
            
        try:
            # 1. Transcribe audio with Whisper
            model = self._get_whisper_model()
            # Force language="es" for faster processing
            segments, info = model.transcribe(temp_audio_path, beam_size=5, language="es")
            raw_transcription = " ".join([segment.text for segment in segments])
            
            # 2. Normalize transcription (No Ollama)
            latex_content = self._normalize_content(raw_transcription)
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                
        inference_time = time.time() - start_time
        return latex_content, raw_transcription, inference_time

    def _process_image_sync(self, temp_image_path: str) -> tuple[str, str]:
        # Preprocesamiento de Imagen (Optimización y Binarización)
        img = Image.open(temp_image_path)
        img = img.convert("RGB")
        img = ImageOps.autocontrast(img)
        
        if img.width > 1600:
            ratio = 1600 / img.width
            new_height = int(img.height * ratio)
            resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
            img = img.resize((1600, new_height), resample_filter)
            
        # Aplicar Otsu Binarization para mejorar manuscritos sin cargar OpenCV en el arranque.
        gray = np.array(ImageOps.grayscale(img))
        binary = self._otsu_threshold(gray)
        img_bin = Image.fromarray(binary)
            
        # Paso 1 (OCR de Texto): pytesseract con optimización para manuscritos usando la imagen binarizada
        import pytesseract

        try:
            text_ocr = pytesseract.image_to_string(img_bin, lang="spa+eng", config="--psm 6").strip()
        except Exception:
            text_ocr = pytesseract.image_to_string(img_bin, config="--psm 6").strip()
            
        # Paso 2 (OCR de Matemáticas): usando la imagen original mejorada (no la binarizada pesada que puede romper pix2tex)
        model = self._get_latex_ocr_model()
        latex_ocr = model(img)
        
        # Paso 3 (Filtro de Alucinación)
        hallucination = False
        tokens_to_check = [r'\omega', r'\mathrm', r'\alpha', r'\beta', r'I', r'1', r'|', r'\\']
        for token in tokens_to_check:
            if latex_ocr.count(token) > 4:
                hallucination = True
                break
                
        if hallucination:
            latex_ocr = "[RUIDO DESCARTADO]"
            
        # Heurística de Detección de Basura (Pre-Ollama)
        import re
        def is_garbage(text: str) -> bool:
            if not text.strip():
                return True
            if len(text.strip()) < 5:
                return True
            
            letters = len(re.findall(r'[a-zA-Z0-9]', text))
            specials = len(re.findall(r'[@#\|><~`_]', text))
            
            # Si hay más de la mitad de caracteres especiales (ruido puro) comparado con letras
            if letters == 0 and specials > 0:
                return True
            if letters > 0 and (specials / letters) > 0.5:
                return True
                
            return False

        error_msg = ""

        if is_garbage(text_ocr) and (latex_ocr == "[RUIDO DESCARTADO]" or is_garbage(latex_ocr)):
            return error_msg, text_ocr
            
        # Paso 4: Fusión directa sin Ollama
        if latex_ocr == "[RUIDO DESCARTADO]" or is_garbage(latex_ocr):
            # Si el LaTeX es ruido, solo devolvemos el texto del OCR
            final_result = self._normalize_content(text_ocr)
        else:
            # Si ambos tienen contenido, entrégalos concatenados
            final_result = self._normalize_content(f"{text_ocr}\n\n$${latex_ocr}$$")
            
        return final_result, text_ocr

    async def process_image(self, file_content: bytes, filename: str) -> tuple[str, str, float]:
        start_time = time.time()
        
        # Save image to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_image_file:
            temp_image_file.write(file_content)
            temp_image_path = temp_image_file.name
            
        try:
            # Execute heavy logic with a 15-second timeout
            task = asyncio.to_thread(self._process_image_sync, temp_image_path)
            latex_content, raw_transcription = await asyncio.wait_for(task, timeout=60.0)
        except asyncio.TimeoutError:
            latex_content = ""
            raw_transcription = "Timeout (30s)"
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing image: {str(e)}"
            )
        finally:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
                
        inference_time = time.time() - start_time
        return latex_content, raw_transcription, inference_time

    async def process_document(self, file_content: bytes, filename: str) -> tuple[str, str, float]:
        start_time = time.time()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_content)
            temp_pdf_path = temp_pdf.name
            
        try:
            import fitz  # PyMuPDF

            # PyMuPDF to extract text
            doc = fitz.open(temp_pdf_path)
            extracted_text = []
            
            for page in doc:
                # Extract clean text, ignoring image layers
                text = page.get_text("text")
                extracted_text.append(text)
                
            raw_transcription = "\n".join(extracted_text)
            
            # 2. Normalize document text (No Ollama)
            latex_content = self._normalize_content(raw_transcription)
            
        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
                
        inference_time = time.time() - start_time
        return latex_content, raw_transcription, inference_time

# Singleton instance for dependency injection
@lru_cache()
def get_multimodal_service() -> MultimodalService:
    return MultimodalService()
