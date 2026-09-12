# Aider RAG API - Использование

## Эндпоинты

### `/api/rag/analyze` - Анализ запроса

```bash
curl -X POST http://localhost:8000/api/rag/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "add new endpoint for user authentication",
    "categories": ["backend", "security"]
  }'
```

**Response:**
```json
{
  "categories": ["backend", "security"],
  "relevant_rules": [
    "/path/to/backend.md",
    "/path/to/security.md"
  ],
  "embedding_available": true,
  "api_version": "1.0.0"
}
```

### `/api/rag/rebuild` - Пересоздание векторного хранилища

```bash
curl -X POST http://localhost:8000/api/rag/rebuild
```

**Response:**
```json
{
  "message": "Векторное хранилище пересоздано",
  "index_updated": false,
  "timestamp": "2024-01-06T12:00:00Z"
}
```

### `/api/rag/health` - Проверка здоровья API

```bash
curl http://localhost:8000/api/rag/health
```

## Интроспекция кодовой базы

Используйте `/api/rag/analyze` для анализа запроса, затем вызовите Aider с релевантными правилами:

```python
from aider_rag import AiderRAG

rag = AiderRAG()
rag.load_or_create_vectorstore()  # Загрузка правил

result = rag.analyze_query("create user registration endpoint")
relevant_files = result["relevant_rules"]

rag.run_aider(result["request"], files=["backend/main.py"])
```

## Интроспекция: как работает RAG система

### 1. Локализация роутов
Система сканирует `backend/routes/` для локализации роутов по ключевым словам (FastAPI, endpoints).

### 2. Анализирует структуру проекта
```python
# Интроспекция
project_info = {
    "routing_pattern": "backend routes",
    "file_structure": "backend/main.py -> router modules",
    "model_location": "models/*.py or ai/*."
}
```

### 3. Создает векторное хранилище
При наличии Ollama/embedding модель создает индекс правил.

### 4. Фоллбэк на ключевые слова
Если API недоступно:
```python
# Keyword matching fallback
if not api_available:
    use_keyword_matching(categories)
```

## Fallback режим

Если Docker не найден или Chroma недоступен, система автоматически переключится на:
- HTTP API запросы (если настроены)
- Keyword matching для категоризации вопросов
- Простой поиск по категориям
