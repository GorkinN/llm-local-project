# aider_rag.py - с qwen2.5-coder:14b для анализа
import sys
import subprocess
from pathlib import Path
from typing import List, Dict
import json
import re
import os
import shutil
import gc
import time

# Отключаем телеметрию
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class AiderRAG:
    def __init__(self):
        """Инициализация RAG системы для Aider"""
        self.rules_dir = Path("docs/rules")
        self.vectorstore_dir = Path(".aider_rag")
        
        print("🔧 Инициализация моделей...")
        
        # Для эмбеддингов - маленькая модель
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        
        # Для анализа запроса - мощная модель
        self.llm = OllamaLLM(
            model="qwen2.5-coder:14b",  # Используем 14b модель
            base_url="http://localhost:11434",
            temperature=0.1,
            timeout=120,
            num_predict=100,  # Ограничиваем длину ответа
        )
        
        print("✅ Модели загружены (qwen2.5-coder:14b для анализа)")
        self.vectorstore = None
    
    def close_vectorstore(self):
        """Закрывает соединение с векторным хранилищем"""
        if self.vectorstore:
            try:
                del self.vectorstore
                self.vectorstore = None
                gc.collect()
                time.sleep(1)
            except Exception:
                pass
    
    def load_or_create_vectorstore(self):
        """Загружает или создает векторное хранилище правил"""
        if self.vectorstore_dir.exists() and (self.vectorstore_dir / "chroma.sqlite3").exists():
            print("📚 Загружаю существующее векторное хранилище...")
            try:
                self.vectorstore = Chroma(
                    persist_directory=str(self.vectorstore_dir),
                    embedding_function=self.embeddings
                )
                print("✅ Векторное хранилище загружено")
            except Exception as e:
                print(f"⚠️ Ошибка загрузки: {e}")
                print("🔄 Создаю новое хранилище...")
                self.create_vectorstore()
        else:
            print("🔨 Создаю новое векторное хранилище правил...")
            self.create_vectorstore()
    
    def create_vectorstore(self):
        """Создает векторное хранилище из файлов правил"""
        documents = []
        
        if not self.rules_dir.exists():
            print(f"❌ Директория {self.rules_dir} не найдена!")
            print("Создайте директорию docs/rules/ и добавьте туда файлы с правилами")
            sys.exit(1)
        
        rule_files = list(self.rules_dir.glob("*.md"))
        if not rule_files:
            print("❌ Нет файлов правил в docs/rules/")
            sys.exit(1)
        
        for rule_file in rule_files:
            try:
                content = rule_file.read_text(encoding='utf-8')
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=150,
                    chunk_overlap=20,
                    separators=["\n\n", "\n", ". ", " ", ""]
                )
                chunks = text_splitter.split_text(content)
                
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
            print("❌ Не удалось загрузить документы")
            sys.exit(1)
        
        print(f"📄 Загружено {len(documents)} чанков из {len(rule_files)} файлов правил")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=str(self.vectorstore_dir)
        )
        print("✅ Векторное хранилище создано")
    
    def analyze_query(self, query: str) -> Dict[str, any]:
        """Анализирует запрос и определяет контекст"""
        # Сначала быстрый keyword matching
        keyword_result = self.keyword_fallback(query)
        
        # Если keyword matching нашел конкретные категории - используем их
        if keyword_result["categories"] != ["general"]:
            print("⚡ Keyword matching нашел категории")
            return keyword_result
        
        # Иначе используем мощную LLM для анализа
        print("🤔 Анализирую запрос с помощью qwen2.5-coder:14b...")
        
        prompt = f"""Проанализируй запрос разработчика и определи, какие категории правил нужны.

Запрос: {query}

Доступные категории:
- backend: FastAPI, endpoints, API, Pydantic, async
- testing: pytest, тесты, coverage, mocking
- ai: Ollama, LLM, модели, генерация
- frontend: React, HTML, CSS, JavaScript
- security: безопасность, аутентификация, CORS
- database: SQLAlchemy, базы данных, репозитории
- performance: производительность, кэширование, оптимизация
- git: git, коммиты, ветки, PR

Верни JSON с полем "categories" - список категорий через запятую.
Например: {{"categories": "backend,security"}}

Только JSON, без дополнительного текста.
"""
        
        try:
            response = self.llm.invoke(prompt)
            print(f"📝 Ответ модели: {response[:200]}...")
            
            # Извлекаем JSON из ответа
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                categories = data.get("categories", "").split(",")
                categories = [cat.strip() for cat in categories if cat.strip()]
                
                if categories:
                    return {
                        "categories": categories,
                        "raw_response": response
                    }
        except Exception as e:
            print(f"⚠️ Ошибка LLM анализа: {e}")
        
        # Fallback на keyword matching
        print("⚡ Fallback на keyword matching")
        return keyword_result
    
    def keyword_fallback(self, query: str) -> Dict[str, any]:
        """Keyword matching для определения категорий"""
        keyword_map = {
            "backend": ["fastapi", "endpoint", "api", "pydantic", "async", "route", "rest", "бэкенд", "бекенд"],
            "testing": ["test", "pytest", "coverage", "mock", "fixture", "тест", "тестировани"],
            "ai": ["ollama", "llm", "model", "generate", "ai", "prompt", "модел", "генерац"],
            "frontend": [
                "react", "html", "css", "js", "javascript", "typescript", "frontend", 
                "ui", "интерфейс", "фронтенд", "веб", "web", "компонент", "component",
                "tailwind", "верстка", "стили", "styles", "axios", "websocket",
                "браузер", "browser", "dom", "responsive", "адаптив"
            ],
            "security": ["security", "auth", "cors", "validation", "token", "безопасн", "аутентифик"],
            "database": ["sqlalchemy", "database", "sql", "repository", "orm", "баз данных", "бд"],
            "performance": ["performance", "cache", "optimiz", "streaming", "производительн", "оптимизац", "кэшир"],
            "git": ["git", "commit", "branch", "merge", "pr", "коммит", "ветк"]
        }
        
        query_lower = query.lower()
        categories = []
        
        for category, keywords in keyword_map.items():
            if any(keyword in query_lower for keyword in keywords):
                categories.append(category)
        
        return {
            "categories": categories or ["general"],
            "raw_response": "keyword matching"
        }
    
    def find_relevant_rules(self, query: str, categories: List[str], k: int = 3) -> List[str]:
        """Находит релевантные правила через векторный поиск"""
        if not self.vectorstore:
            return []
        
        enhanced_query = f"{query} {' '.join(categories)}"
        
        try:
            results = self.vectorstore.similarity_search_with_score(
                enhanced_query,
                k=k
            )
        except Exception as e:
            print(f"⚠️ Ошибка поиска: {e}")
            return []
        
        rules = []
        seen = set()
        
        for doc, score in results:
            source = doc.metadata.get("source", "")
            if source and source not in seen:
                seen.add(source)
                rules.append(source)
                
                # Добавляем связанные правила по категориям
                for category in categories:
                    category_file = self.rules_dir / f"{category}.md"
                    if category_file.exists() and str(category_file) not in seen:
                        seen.add(str(category_file))
                        rules.append(str(category_file))
        
        return rules[:5]
    
    def run_aider(self, query: str, files: List[str] = None):
        """Запускает Aider в Docker с релевантными правилами"""
        print("\n" + "="*60)
        print("🤖 Анализ запроса...")
        
        analysis = self.analyze_query(query)
        categories = analysis["categories"]
        print(f"📋 Определены категории: {', '.join(categories)}")
        
        rules = self.find_relevant_rules(query, categories)
        
        if rules:
            print(f"📚 Подобраны правила:")
            for rule in rules:
                print(f"  - {rule}")
        else:
            print("⚠️ Правила не найдены")
        
        # Формируем команду для Docker
        current_dir = os.getcwd()
        
        cmd_parts = [
            "docker", "run", "-it", "--rm",
            "--gpus", "all",
            "-v", f"{current_dir}:/app",
            "-e", "OLLAMA_API_BASE=http://host.docker.internal:11434",
            "aider-full",  
        ]
        
        # Добавляем файлы если есть
        if files:
            # Конвертируем пути для Docker
            docker_files = []
            for f in files:
                # Убираем текущую директорию из пути
                f_clean = f.replace(current_dir, "").lstrip("\\/")
                docker_files.append(f_clean)
            cmd_parts.extend(docker_files)
        
        # Добавляем правила
        for rule in rules:
            # Конвертируем Windows путь в Docker путь
            docker_rule = rule.replace("\\", "/")
            # Убираем текущую директорию
            docker_rule = docker_rule.replace(current_dir.replace("\\", "/"), "").lstrip("/")
            # Добавляем /app/
            docker_rule = "/app/" + docker_rule
            cmd_parts.extend(["--read", docker_rule])
        
        # Добавляем запрос
        cmd_parts.extend(["--message", query])
        
        print(f"🔧 Docker команда:")
        print(f"   docker run -it --rm --gpus all -v {current_dir}:/app ...")
        print("\n🚀 Запускаю Aider в Docker...")
        print("="*60 + "\n")
        
        try:
            subprocess.run(cmd_parts)
        except FileNotFoundError:
            print("❌ Docker не найден!")
            print("Установите Docker Desktop или запустите Docker")
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")
    
    def rebuild(self):
        """Пересоздает векторное хранилище"""
        self.close_vectorstore()
        
        if self.vectorstore_dir.exists():
            try:
                shutil.rmtree(self.vectorstore_dir)
                print("✅ Старое хранилище удалено")
            except PermissionError as e:
                print(f"⚠️ Не удалось удалить: {e}")
                print("💡 Удалите вручную: Remove-Item .aider_rag -Recurse -Force")
                sys.exit(1)
        
        self.create_vectorstore()
        print("✅ Векторное хранилище пересоздано")

def main():
    if len(sys.argv) < 2:
        print("""
📚 Aider RAG - умный подбор правил для Aider

Использование:
  python aider_rag.py "ваш запрос для Aider"
  python aider_rag.py "запрос" --files backend/main.py ai/llm.py
  python aider_rag.py --rebuild
""")
        sys.exit(1)
    
    args = sys.argv[1:]
    rebuild = False
    files = []
    query_parts = []
    
    i = 0
    while i < len(args):
        if args[i] == "--rebuild":
            rebuild = True
        elif args[i] == "--files":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                files.append(args[i])
                i += 1
            continue
        elif not args[i].startswith("--"):
            query_parts.append(args[i])
        i += 1
    
    query = " ".join(query_parts)
    
    if not query and not rebuild:
        print("❌ Укажите запрос")
        sys.exit(1)
    
    rag = AiderRAG()
    
    if rebuild:
        rag.rebuild()
        sys.exit(0)
    
    rag.load_or_create_vectorstore()
    rag.run_aider(query, files)

if __name__ == "__main__":
    main()