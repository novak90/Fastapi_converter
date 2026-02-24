from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import JSONResponse, Response
import xmltodict

# Создаём роутер
router = APIRouter()

def parse_soap_body(body: bytes) -> dict:
    """Преобразует SOAP (XML) в словарь Python"""
    try:
        xml_str = body.decode('utf-8')
        data = xmltodict.parse(xml_str)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга XML/SOAP: {str(e)}")

def dict_to_xml(data: dict) -> str:
    """Преобразует словарь обратно в XML"""
    try:
        return xmltodict.unparse(data, pretty=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка формирования XML: {str(e)}")

@router.post("")
async def convert_soap(
    request: Request,
    format: str = Query("json", regex="^(json|xml)$", description="Формат ответа: json или xml")
):
    """Единый эндпоинт для конвертации SOAP -> JSON или XML"""
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Тело запроса не может быть пустым")

    # Парсим SOAP в Python-объект
    parsed_data = parse_soap_body(body)

    if format == "json":
        return JSONResponse(content=parsed_data)
    else:  # format == "xml"
        xml_output = dict_to_xml(parsed_data)
        return Response(content=xml_output, media_type="application/xml")

@router.post("/extract")
async def extract_soap_body(request: Request):
    """Извлекает содержимое SOAP-тела"""
    body = await request.body()
    parsed = parse_soap_body(body)

    # Пытаемся добраться до содержимого SOAP-тела
    try:
        envelope = parsed.get('soap:Envelope', parsed.get('Envelope', {}))
        body_content = envelope.get('soap:Body', envelope.get('Body', {}))
        if body_content:
            return JSONResponse(content=body_content)
        else:
            return JSONResponse(content=parsed)
    except Exception:
        return JSONResponse(content=parsed)