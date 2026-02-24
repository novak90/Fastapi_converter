from fastapi import FastAPI
from app.xml import router as soap_router
from app.rest import router as rest_router  # новый импорт

app = FastAPI(
    title="SOAP/JSON Converter",
    description="Конвертер между SOAP и JSON",
    version="1.0.0"
)

# Подключаем оба роутера
app.include_router(soap_router, prefix="/soap", tags=["soap"])
app.include_router(rest_router, prefix="/rest", tags=["rest"])  # новый роутер

@app.get("/")
async def root():
    return {
        "message": "Converter by Брат Валера",
        "endpoints": {
            "/soap": "POST: Принимает SOAP, возвращает JSON",
            "/soap?format=xml": "POST: Принимает SOAP, возвращает XML",
            "/rest": "POST: Принимает JSON, возвращает SOAP",
            "/docs": "Документация Swagger"
        }
    }