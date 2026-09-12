# LLM Local Project - RAG Система для Aider

## Локализация роутов

**Backend:** `backend/routes/` — основные роуты с текстовой генерацией (`generate.py`)  
**Frontend:** `frontend/` — React приложения

## 📚 Aider RAG API

Умный подбор правил для продакшена через HTTP API (без Docker зависимостей):

### Эндпоинты

#### `/api/rag/analyze`
Анализирует запрос и определяет релевантные категории правил:
```bash
curl -X POST http://localhost:8000/api/rag/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "create user registration endpoint"}'
```

**Response:**
```json
{
  "categories": ["backend", "security"],
  "relevant_rules": [...],
  "embedding_available": true
}
```

#### `/api/rag/rebuild`
Пересоздает векторное хранилище (опционально):
```bash
curl -X POST http://localhost:8000/api/rag/rebuild
```

#### `/api/rag/health`
Проверка здоровья API:
```bash
curl http://localhost:8000/api/rag/health
```

### Интроспекция кодовой базы

**Локализация роутов:**
- Сканирует `backend/routes/` для определения модели роутинга
- Анализирует существующие роуты: FastAPI, endpoints
- Ищет паттерны генерации текста/изображений

**Интроспекция:**
- Определяет структуру проекта (frontend/backend)
- Находит AI компоненты в `ai/.py` или `models/.py`
- Создает релевантный контекст для генерации по запросу

### Fallback режим

Если Ollama/embedding недоступно:
- Используется keyword matching для категоризации
- Простой поиск по категориям вместо векторного поиска

## Файлы правил

**Расположение:** `docs/rules/`  
**Формат:** `*.md` файлы с описанием паттернов

**Категории:**
- `ai.md` - LLM, embedding, prompts
- `backend.md` - роуты, endpoints, FastAPI
- `frontend.md` - React, HTML/CSS
- `performance.md` - оптимизация
- `security.md` - auth, CORS, токены
- `testing.md` - pytest, coverage

## Пример запуска Aider

```python
from aider_rag import AiderRAG

rag = AiderRAG()
rag.load_or_create_vectorstore()
result = rag.analyze_query("add user registration endpoint")
rag.run_aider(result["request"], files=["backend/main.py"])
```
