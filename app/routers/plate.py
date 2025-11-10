from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from app.uteis import distancia_ponderada, save_uploaded_image_as_png, get_plate_text
from fastapi import WebSocket
import asyncio
from app.mqtt_client import mqttc 

connections = []

router = APIRouter(
    prefix="/plate",
    tags=["plate"],
    responses={404: {"description": "Not found"}},
)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    print(f"Cliente conectado: {websocket.client}")
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Cliente desconectado: {websocket.client}")
    finally:
        if websocket in connections:
            connections.remove(websocket)

@router.post("/validate")
async def validate_plate_image(
    file: UploadFile = File(...),
    id: str = None,
    status: str = None
):

    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Arquivo de imagem inválido.")
    
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Nenhuma imagem enviada.")
    
    if status not in ['LIVRE', 'OCUPADO']:
        raise HTTPException(status_code=400, detail="Status inválido.")
    
    await save_uploaded_image_as_png(file, id)

    plate = await get_plate_text(file)

    plate_valida = 'BEE4R2P' # Pegar do banco baseado no id do spot e dia da semana
    
    is_valid = distancia_ponderada(plate_valida, plate['plate'])

    disconnected = []
    for connection in connections:
        try:
            await connection.send_json({
                "plate_ocr": plate['plate'],
                "plate_db": plate_valida,
                "status": status,
                "id": id,
                "valid": is_valid
            })
        except Exception:
            disconnected.append(connection)

    for dc in disconnected:
        if dc in connections:
            connections.remove(dc)


    return Response(status_code=204)

@router.post("/take_picture/{spot_id}/{command}")
def enviar_comando(spot_id: str, command: str):
    topic = f"api_vision/spot/{spot_id}"
    mqttc.publish(topic, command)
    print(f"Publicado no tópico {topic} o comando: {command}")
    return {"status": "ok", "topico": topic, "comando": command}
