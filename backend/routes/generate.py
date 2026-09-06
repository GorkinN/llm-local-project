from fastapi import APIRouter, HTTPException
from backend.services.llm_service import generate_text, generate_image

router = APIRouter()

@router.post("/generate")
async def generate_text_endpoint(prompt: str):
    try:
        response = await generate_text(prompt)  # Add await here
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/image")
async def generate_image_endpoint(prompt: str):
    try:
        response = await generate_image(prompt)  # Add await here
        return {"generated_image_url": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
