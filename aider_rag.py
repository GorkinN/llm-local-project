# aider_rag.py - умный подбор правил
import subprocess
from pathlib import Path
from typing import List, Dict
import json
import re
import os

class AiderRAG:
    """Умный подбор правил для продакшена (через HTTP API)"""

    def __init__(self, config=None):
        self.rules_dir = Path("docs/rules")
        self._config = config or {}
        self.rag_api_available = True  # По умолчанию используем API (prod)
        
        print("🔧 Andex AiderRAG...")

    def load_or_create_vectorstore(self):
        """Загружает правила для анализа"""
        # В режиме API продакшена (без Docker) не нужен vectorstore
        if not self.rag_api_available:
            return []
        
        if not self.rules_dir.exists():
            print("❌ Директория docs/rules/ не найдена")
            return []
        
        rule_files = list(self.rules_dir.glob("*.md"))
        if not rule_files:
            print("❌ Нет файлов правил")
            return []
        
        print(f"📚 Найдено {len(rule_files)} файлов правил")
        return [str(r) for r in rule_files]

    def analyze_query(self, query: str) -> Dict[str, any]:
        """Анализирует запрос и определяет контекст"""
        # Быстрый keyword matching (fallback)
        result = self.keyword_fallback(query)
        categories = result.get("categories", ["general"])
        
        print(f"📋 Определены категории: {', '.join(categories)}")
        return result

    def keyword_fallback(self, query: str) -> Dict[str, any]:
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
        
        return {
            "categories": categories or ["general"],
            "raw_response": "keyword matching"
        }

    def find_relevant_rules(self, query: str, k: int = 5) -> List[str]:
        """Ищет похожие правила (упрощенно через keyword + файлы категорий)"""
        result = self.analyze_query(query)
        categories = result.get("categories", ["general"])
        
        rules = []
        seen = set()
        
        for category in categories:
            f_name = self.rules_dir / f"{category}.md"
            if f_name.exists():
                f_path = str(f_name)
                if f_path not in seen:
                    seen.add(f_path)
                    rules.append(f_path)
        
        return rules[:k]

    def run_aider(self, query: str, files: List[str] = None):
        """Запускает Aider в Docker с релевантными правилами"""
        print("\n" + "="*60)
        print("🤖 Запуск Aider в Docker...")
        
        current_dir = os.getcwd()
        
        # Подготовка файлов для Docker
        docker_files = []
        for f in files or []:
            f_clean = f.replace(current_dir, "").lstrip("\\/")
            docker_files.append(f_clean)
        
        # Подготовка правил
        rules = self.find_relevant_rules(query)
        
        cmd_parts = [
            "docker", "run", "-it", "--rm",
            "--gpus", "all",
            "-v", f"{current_dir}:/app",
            "-e", "OLLAMA_API_BASE=http://host.docker.internal:11434",
            "aider-full"  
        ]
        
        # Добавляем файлы если есть
        if docker_files:
            cmd_parts.extend(docker_files)
        
        # Добавляем правила
        for rule in rules:
            docker_rule = "/app/" + rule.lstrip("/")
            cmd_parts.extend(["--read", docker_rule])
        
        # Добавляем запрос
        cmd_parts.extend(["--message", query])
        
        print(f"🔧 Docker команда: {' '.join(cmd_parts)}")
        
        try:
            subprocess.run(cmd_parts)
        except FileNotFoundError:
            print("❌ Docker не найден!")
            print("Установите Docker Desktop")
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")
    
    def rebuild(self):
        """Пересоздает векторное хранилище"""
        print("В режиме API пересоздание не требуется")


def main():
    if len(sys.argv) < 2:
        print("""
📚 Aider RAG - умный подбор правил для продакшена

Использование:
  python aider_rag.py "ваш запрос для Aider"
  python aider_rag.py "запрос" --files backend/main.py ai/llm.py
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
    
    if rag.rag_api_available:
        rules = rag.load_or_create_vectorstore()
        if not rules:
            print("⚠️ Правила не найдены")
        else:
            rag.run_aider(query, files)

if __name__ == "__main__":
    import sys
    main()
