# Регистрация маршрутов FastAPI отладка
from fastapi import APIRouter

# Подключаем роуты текстовой генерации
from backend.routes.generate import router as text_router

# Подключаем роут для RAG операций
try:
    from backend.routes.rag import router as rag_router
except ImportError as e:
    print(f"⚠️ Cannot load RAG routes: {e}")
    rag_router = APIRouter(prefix="/")  # fallback empty router

# Объединяем все маршруты
api_router = APIRouter()
api_router.include_router(text_router)
api_router.include_router(rag_router)
