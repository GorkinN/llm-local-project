from .image_generation import router as image_generation_router

app.include_router(image_generation_router, prefix="/image", tags=["image"])
