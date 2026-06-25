from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.schemas.multimodal import MultimodalResponse
from app.services.multimodal_service import MultimodalService, get_multimodal_service

router = APIRouter()

@router.post("/audio", response_model=MultimodalResponse)
async def process_audio_endpoint(
    file: UploadFile = File(...),
    multimodal_service: MultimodalService = Depends(get_multimodal_service)
):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported audio format. Use .wav, .mp3, or .m4a."
        )
        
    content = await file.read()
    latex, raw, time_taken = await multimodal_service.process_audio(content, file.filename)
    
    return MultimodalResponse(
        status="success",
        file_type="audio",
        latex_content=latex,
        raw_transcription=raw,
        metadata={"inference_time": time_taken}
    )

@router.post("/image", response_model=MultimodalResponse)
async def process_image_endpoint(
    file: UploadFile = File(...),
    multimodal_service: MultimodalService = Depends(get_multimodal_service)
):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported image format."
        )
        
    content = await file.read()
    latex, raw, time_taken = await multimodal_service.process_image(content, file.filename)
    
    return MultimodalResponse(
        status="success",
        file_type="image",
        latex_content=latex,
        raw_transcription=raw,
        metadata={"inference_time": time_taken}
    )

@router.post("/document", response_model=MultimodalResponse)
async def process_document_endpoint(
    file: UploadFile = File(...),
    multimodal_service: MultimodalService = Depends(get_multimodal_service)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported document format. Use .pdf."
        )
        
    content = await file.read()
    latex, raw, time_taken = await multimodal_service.process_document(content, file.filename)
    
    return MultimodalResponse(
        status="success",
        file_type="document",
        latex_content=latex,
        raw_transcription=raw,
        metadata={"inference_time": time_taken}
    )
