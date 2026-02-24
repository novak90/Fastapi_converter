from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
import xmltodict
from typing import Any, Dict, Optional

router = APIRouter()

# Pydantic модели для запросов - именно они появятся в Swagger!
class SimpleJsonRequest(BaseModel):
    """
    Произвольный JSON для конвертации в SOAP.
    Может содержать любые поля.
    """
    data: Dict[str, Any] = Field(
        default={"city": "Moscow", "temperature": 20},
        description="Любые данные для конвертации в SOAP. Будут обернуты в тег <Request>"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "Moscow",
                "temperature": 20,
                "units": "Celsius"
            }
        }

class CustomJsonRequest(BaseModel):
    """
    JSON для кастомного SOAP-запроса с указанием имени корневого элемента.
    """
    root_element: str = Field(
        ...,
        description="Имя корневого элемента в SOAP Body",
        example="GetWeather"
    )
    data: Dict[str, Any] = Field(
        ...,
        description="Данные запроса",
        example={"City": "Moscow", "Units": "Celsius"}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "root_element": "GetWeather",
                "data": {
                    "City": "Moscow",
                    "Units": "Celsius"
                }
            }
        }

def json_to_soap(json_data: dict, root_name: str = "Request") -> str:
    """Преобразует JSON в SOAP (XML) с указанным корневым элементом"""
    try:
        soap_envelope = {
            "soap:Envelope": {
                "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
                "soap:Body": {
                    root_name: json_data
                }
            }
        }
        return xmltodict.unparse(soap_envelope, pretty=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка формирования SOAP: {str(e)}")

@router.post(
    "",
    response_class=Response,
    responses={
        200: {
            "content": {"application/xml": {}},
            "description": "Успешный ответ в формате SOAP (XML)"
        },
        400: {
            "description": "Неверный JSON"
        }
    },
    summary="Конвертировать JSON в SOAP",
    description="Принимает JSON и возвращает SOAP (XML) с корневым элементом <Request>"
)
async def convert_json_to_soap(request_data: SimpleJsonRequest):
    """
    Принимает JSON, возвращает SOAP (XML)
    
    - **request_data**: любой JSON-объект, который будет преобразован в SOAP
    """
    # Получаем данные из модели
    data = request_data.data
    
    # Конвертируем в SOAP
    soap_output = json_to_soap(data, "Request")
    return Response(content=soap_output, media_type="application/xml")

@router.post(
    "/custom",
    response_class=Response,
    responses={
        200: {
            "content": {"application/xml": {}},
            "description": "Успешный ответ в формате SOAP (XML)"
        },
        400: {
            "description": "Неверный JSON или отсутствуют обязательные поля"
        }
    },
    summary="Конвертировать JSON в SOAP (кастомный)",
    description="Позволяет указать имя корневого элемента в SOAP Body"
)
async def convert_json_to_soap_custom(request_data: CustomJsonRequest):
    """
    Более гибкая версия: позволяет указать имя корневого элемента.
    
    - **root_element**: имя корневого элемента (например, "GetWeather")
    - **data**: данные запроса
    """
    # Получаем данные из модели
    root_element = request_data.root_element
    data = request_data.data
    
    # Конвертируем в SOAP с указанным корневым элементом
    soap_output = json_to_soap(data, root_element)
    return Response(content=soap_output, media_type="application/xml")