from fastapi import APIRouter

from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from io import BytesIO
import numpy as np
import PIL.Image
from uteis import validate_plate

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

    plate = await validate_plate(img_np)

    return JSONResponse(
        content=plate
    )

