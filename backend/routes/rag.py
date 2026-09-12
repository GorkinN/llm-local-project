from fastapi import APIRouter, HTTPException
from typing import List
import json
import re
from pathlib import Path
import shutil
import subprocess
import gc
import time
from datetime import datetime
from backend.models.schemas import QueryRequest, AnalysisResponse, RebuildRequest

router = APIRouter()


class AiderRAG:
    """Класс RAG системы"""

    def __init__(self):
        self.rules_dir = Path("docs/rules")
        self.vectorstore_dir = Path(".aider_rag")
        
        # Инициализация моделей (для продакшна лучше вынести в конфигурацию)
        try:
            from langchain_ollama import OllamaEmbeddings, OllamaLLM
            
            self.embeddings = OllamaEmbeddings(
                model="nomic-embed-text",
                base_url="http://localhost:11434"
            )
            
            self.llm = OllamaLLM(
                model="qwen2.5-coder:14b",
                base_url="http://localhost:11434",
                temperature=0.1,
                timeout=120,
                num_predict=100,
            )
            self.rag_ready = True
        except Exception as e:
            print(f"⚠️ Модели LLM не доступны: {e}")
            self.rag_ready = False
    
    def load_or_create_vectorstore(self):
        """Загружает или создает векторное хранилище"""
        if not self.rules_dir.exists():
            return None
        
        rule_files = list(self.rules_dir.glob("*.md"))
        if not rule_files:
            return []
        
        documents = []
        for rule_file in rule_files:
            try:
                content = rule_file.read_text(encoding='utf-8')
                from langchain.text_splitter import RecursiveCharacterTextSplitter
                from langchain_core.documents import Document
                
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=150,
                    chunk_overlap=20,
                    separators=["\n\n", "\n", ". ", " ", ""]
                )
                chunks = splitter.split_text(content)
                
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": str(rule_file),
                            "filename": rule_file.stem,
                            "chunk": i
                        }
                    )
                    documents.append(doc)
            except Exception as e:
                print(f"⚠️ Ошибка чтения {rule_file}: {e}")
        
        if not documents:
            return []
        
        try:
            from langchain_chroma import Chroma
            
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=str(self.vectorstore_dir)
            )
            print("✅ Векторное хранилище создано")
        except ImportError:
            print("⚠️ langchain-chroma не установлен")
            return []
        
        return [str(r.metadata["source"]) for r in documents]
    
    def keyword_fallback(self, query: str) -> dict:
        """Keyword matching для определения категорий"""
        keyword_map = {
            "backend": ["fastapi", "endpoint", "api", "pydantic", "async", "route"],
            "testing": ["test", "pytest", "coverage", "mock"],
            "ai": ["ollama", "llm", "model", "generate", "prompt"],
            "frontend": ["react", "html", "css", "js", "javascript", "typescript"],
            "security": ["security", "auth", "cors", "validation", "token"],
            "database": ["sqlalchemy", "database", "sql", "repository", "orm"],
            "performance": ["performance", "cache", "optimiz", "streaming"],
            "git": ["git", "commit", "branch", "merge", "pr"]
        }
        
        query_lower = query.lower()
        categories = []
        
        for category, keywords in keyword_map.items():
            if any(keyword in query_lower for keyword in keywords):
                categories.append(category)
        
        return {"categories": categories or ["general"], "raw_response": "keyword matching"}
    
    def analyze_query(self, query: str, use_llm: bool = True) -> dict:
        """Анализирует запрос и определяет контекст"""
        # Быстрый keyword matching
        result = self.keyword_fallback(query)
        
        if not self.rag_ready or not use_llm:
            return result
        
        # Использовать LLM для анализа (если модели доступны)
        try:
            prompt = f"""Проанализируй запрос разработчика и определи категории.

Запрос: {query}

Возможные категории: backend, testing, ai, frontend, security, database, performance, git

Верни только JSON: {{"categories": "категория1,категория2"}}
"""
            response = self.llm.invoke(prompt)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                categories = [cat.strip() for cat in data.get("categories", "").split(",") if cat.strip()]
                return {"categories": categories or ["general"], "raw_response": str(response)}
        except Exception as e:
            print(f"⚠️ Ошибка LLM анализа: {e}")
        
        return self.keyword_fallback(query)


class RAGService(AiderRAG):
    """Упрощенная версия без зависимости от Docker"""

    def __init__(self):
        super().__init__()
        # В режиме продакшна используем простые keyword-запросы
    
    async def find_relevant_rules(self, query: str, categories: list[str], k: int = 5) -> List[Path]:
        """Находит релевантные правила (упрощенная версия без векторного поиска)"""
        rules = []
        
        # Добавляем файлы по категориям если существуют
        for category in categories:
            category_file = self.rules_dir / f"{category}.md"
            if category_file.exists():
                rules.append(category_file)
        
        # Добавляем общий файл правил если есть
        general_file = self.rules_dir / "general.md"
        if general_file.exists():
            rules.append(general_file)
        
        return list(set(rules))[:k]
    
    def analyze_and_prepare(self, query: str, files: List[str] = None):
        """Анализирует запрос и возвращает информацию"""
        analysis = self.analyze_query(query)
        categories = analysis.get("categories", ["general"])
        
        # Ищем релевантные правила
        rules = []
        seen = set()
        for category in categories:
            f_name = self.rules_dir / f"{category}.md"
            if f_name.exists():
                f_path = str(f_name)
                if f_path not in seen:
                    seen.add(f_path)
                    rules.append(f_path)
        
        # Общий файл правил
        gen_file = self.rules_dir / "general.md"
        if gen_file.exists():
            if str(gen_file) not in seen:
                seen.add(str(gen_file))
                rules.append(str(gen_file))
        
        return {
            "categories": categories,
            "rules": rules[:5],  # Возвращаем топ-5 правил
            "raw_response": analysis.get("raw_response", "")
        }


# Глобальный экземпляр RAG сервиса
rag_service = None

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_query_endpoint(request: QueryRequest):
    """Анализирует запрос и подобраные правила"""
    global rag_service
    
    if not rag_service:
        try:
            from backend.services.rag_service import rag_service
        except ImportError:
            rag_service = RAGService()
    
    result = rag_service.analyze_and_prepare(request.query, request.files or [])
    
    return AnalysisResponse(
        categories=result.get("categories", []),
        relevant_rules=result.get("rules", []),
        docker_command=None  # В продакшене не используем Docker
    )


@router.post("/rebuild")
async def rebuild_vectorstore(request: RebuildRequest):
    """Пересоздает векторное хранилище"""
    if not rag_service:
        try:
            from backend.services.rag_service import rag_service
        except ImportError:
            rag_service = RAGService()
    
    if rag_service.vectorstore_dir.exists():
        try:
            shutil.rmtree(rag_service.vectorstore_dir)
            print("✅ Старое хранилище удалено")
        except Exception as e:
            print(f"⚠️ Не удалось удалить хранилище: {e}")
    
    rules = rag_service.load_or_create_vectorstore()
    
    return {
        "status": "success",
        "rules_count": len(rules) if rules else 0,
        "message": "✅ Векторное хранилище пересоздано"
    }


@router.get("/health")
async def health_check():
    """Проверка работоспособности API"""
    return HealthCheckResponse(
        status="ok",
        timestamp=datetime.now()
    )
