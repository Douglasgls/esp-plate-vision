from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Response
from app.uteis import distancia_ponderada, save_uploaded_image_as_png, get_plate_text
from fastapi import WebSocket
import asyncio
from app.mqtt_client import mqttc 
from app.service.spot import SpotService
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import FileResponse
import os

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
    id: str = Form(...),
    status: str = Form(...)
):
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Arquivo de imagem inválido.")
    
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Nenhuma imagem enviada.")
    
    if status.upper() not in ['LIVRE', 'OCUPADO']:
        raise HTTPException(status_code=400, detail="Status inválido.")
    
    filepath = await save_uploaded_image_as_png(file, id)

    print(filepath)

    plate = await get_plate_text(file)

    plate_valida = 'BEE4R2P' # Pegar do banco baseado no id do spot e dia da semana
    
    is_valid = distancia_ponderada(plate_valida, plate['plate'])

    if (is_valid['similaridade_pct'] > 60):
        await SpotService.update_status(id, 'OCUPADO')
        alert = False
    else:
        await SpotService.update_status(id, 'OCUPADO','OCUPADO') 
        alert = True


    disconnected = []
    for connection in connections:
        try:
            await connection.send_json({
                "plate_ocr": plate['plate'],
                "plate_db": plate_valida,
                "status": status.upper(),
                "id": id,
                "is_alert": alert,
                "valid": is_valid,
                "image_url": f"/plate/last_picture/{id}",
                "last_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    
    return {"status": "ok", "topico": topic, "comando": command}

@router.get("/last_picture/{spot_id}")
async def get_last_picture(spot_id: str):
    folder = f"uploads/vaga-{spot_id}"

    if not os.path.isdir(folder):
        raise HTTPException(status_code=404, detail="Pasta não encontrada para este ID.")

    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not files:
        raise HTTPException(status_code=404, detail="Nenhuma imagem encontrada para este ID.")
    
    files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)

    last_file = os.path.join(folder, files[0])

    return FileResponse(last_file, media_type="image/png")

@router.get("/last_picture_info/{spot_id}")
async def get_last_picture_info(spot_id: str):
    folder = f"uploads/vaga-{spot_id}"

    if not os.path.isdir(folder):
        raise HTTPException(status_code=404, detail="Pasta não encontrada para este ID.")

    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not files:
        raise HTTPException(status_code=404, detail="Nenhuma imagem encontrada para este ID.")
    
    files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)

    last_file = files[0]
    file_path = os.path.join(folder, last_file)

    timestamp = os.path.getmtime(file_path)

    return {
        "image_url": f"/plate/last_picture/{spot_id}",
        "filename": last_file,
        "timestamp": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    }
