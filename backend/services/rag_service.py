"""Сервис работы с RAG системой (упрощенная версия для продакшена)"""

from pathlib import Path
import json
import re
from typing import List, Dict, Optional


class RAGService:
    """Упрощенный сервис RAG без зависимости от Docker и LangChain"""

    def __init__(self):
        self.rules_dir = Path("docs/rules")
        self.vectorstore_dir = Path(".aider_rag")
        
    def load_or_create_vectorstore(self):
        """Загружает или создает векторное хранилище (placeholder)"""
        if not self.rules_dir.exists():
            return None
        
        rule_files = list(self.rules_dir.glob("*.md"))
        if not rule_files:
            return []
        
        print(f"📚 Найдено {len(rule_files)} файлов правил")
        return [str(r) for r in rule_files]

    def keyword_fallback(self, query: str) -> dict:
        """Keyword matching для определения категорий"""
        query_lower = query.lower()
        
        categories = []
        
        if any(kw in query_lower for kw in ["fastapi", "endpoint", "api", "route"]):
            categories.append("backend")
        if any(kw in query_lower for kw in ["test", "pytest", "coverage"]):
            categories.append("testing")
        if any(kw in query_lower for kw in ["ollama", "llm", "model", "prompt"]):
            categories.append("ai")
        if any(kw in query_lower for kw in ["react", "html", "css", "javascript", "frontend"]):
            categories.append("frontend")
        if any(kw in query_lower for kw in ["security", "auth", "cors", "token"]):
            categories.append("security")
        if any(kw in query_lower for kw in ["database", "sql", "repotitory", "orm"]):
            categories.append("database")
        if any(kw in query_lower for kw in ["performance", "cache", "optimiz"]):
            categories.append("performance")
        
        return {"categories": categories or ["general"], "raw_response": "keyword matching"}

    def analyze_query(self, query: str) -> dict:
        """Анализирует запрос и определяет категории"""
        analysis = self.keyword_fallback(query)
        categories = analysis.get("categories", ["general"])
        
        print(f"📋 Определили категории: {', '.join(categories)}")
        return analysis

    def find_relevant_rules(self, query: str, categories: List[str], k: int = 5) -> List[Path]:
        """Находит релевантные правила"""
        rules = []
        
        for category in categories:
            # Ищем файл по категории
            category_file = self.rules_dir / f"{category}.md"

# Экземпляр сервиса (инициализируется при первом обращении)
rag_service = RAGService()
