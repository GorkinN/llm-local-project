from fastapi import FastAPI
from backend.routes.generate import router as generate_router
from backend.routes.rag import router as rag_router

app = FastAPI(
    title="LLM API",
    description="API для текстовой генерации и RAG-анализа",
    version="2.0"
)

# Генерация текста и изображений
app.include_router(generate_router, prefix="/api", tags=["generate"])

# RAG операции (анализ запросов)
app.include_router(rag_router, prefix="/api", tags=["rag"])

@app.get("/health", tags=["Health"])
async def health_check_endpoint():
    """Проверка работоспособности"""
    return {"status": "ok", "timestamp": "now"}
