from fastapi import APIRouter, Request

from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from io import BytesIO
import numpy as np
import PIL.Image
from app.uteis import get_plate_info, distancia_ponderada
from PIL import Image
import io
from datetime import datetime


router = APIRouter(
    prefix="/plate",
    tags=["plate"],
    responses={404: {"description": "Not found"}},
)

@router.post("/validate")
async def validate_plate_image(file: UploadFile = File(...)):
    contents = await file.read()

    image = PIL.Image.open(BytesIO(contents)).convert("RGB")

    img_np = np.array(image)

    plate = await get_plate_info(img_np)

    plate_valida = 'BEE4R2P' #TODO VALOR MOCADO
    is_valid = distancia_ponderada(plate_valida, plate['plate'])

    return JSONResponse(
        {
            "placa_ocr": plate['plate'], 
            "similaridade": is_valid['similaridade'],
            "similaridade_pct": is_valid['similaridade_pct'],
            "custo_total": is_valid['custo_total'],
            "detalhes": is_valid['detalhes']
        }
    )

@router.post("/uploadfile")
async def create_upload_file(request: Request):
    try:
        data = await request.body()

        image_jpg = Image.open(io.BytesIO(data))

        file_temp_now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"uploads/camera_{file_temp_now}.png" 
        image_jpg.save(filename, format="PNG")

        return {"filename": filename}

    except Image.UnidentifiedImageError:
        return {"error": "Could not identify image file. Check file format/contents."}, 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred"}, 500
