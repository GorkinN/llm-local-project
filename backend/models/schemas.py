from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class QueryRequest(BaseModel):
    """Запрос для анализа"""
    query: str = Field(..., description="Вопрос или запрос разработчика")
    files: list[str] = Field(default_factory=list, description="Файлы для контекста (опционально)")


class AnalysisResponse(BaseModel):
    """Ответ с результатами анализа"""
    categories: list[str] = Field(description="Найденные категории")
    relevant_rules: list[str] = Field(description="Подобраные правила")
    docker_command: Optional[str] = Field(None, description="Готовая команда Docker")


class RebuildRequest(BaseModel):
    """Запрос на пересоздание векторного хранилища"""
    force: bool = Field(default=False, description='Принудительное создание хранилища')


class HealthCheckResponse(BaseModel):
    """Ответ проверки работоспособности"""
    status: str = "ok"
    timestamp: datetime = Field(default_factory=datetime.now)
