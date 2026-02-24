from fastapi import FastAPI
# ИЗМЕНЕНИЕ ЗДЕСЬ: используем абсолютный импорт
from app.xml import router as xml_router

# Создаём экземпляр приложения
app = FastAPI(
    title="SOAP Converter",
    description="Конвертер SOAP-запросов в JSON и XML",
    version="1.0.0"
)

# Подключаем роутер с префиксом /soap
app.include_router(xml_router, prefix="/soap", tags=["soap"])

# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    return {
        "message": "SOAP Converter",
        "endpoints": {
            "/soap": "POST: Принимает SOAP, возвращает JSON (по умолчанию)",
            "/soap?format=json": "POST: Принимает SOAP, возвращает JSON",
            "/soap?format=xml": "POST: Принимает SOAP, возвращает XML",
            "/docs": "Документация Swagger",
            "/redoc": "Документация ReDoc"
        }
    }