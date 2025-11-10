from fastapi import APIRouter, Request, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from io import BytesIO
import numpy as np
from PIL import Image, UnidentifiedImageError
from datetime import datetime
from app.uteis import get_plate_info, distancia_ponderada



router = APIRouter(
    prefix="/plates",
    tags=["plates"],
    responses={404: {"description": "Not found"}},
)


@router.post("/validate")
async def validate_plate_image(file: UploadFile = File(...)):
    """
    Validate a license plate image by comparing it to a reference plate.
    """
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    img_np = np.array(image)

    plate_info = await get_plate_info(img_np)

    mocked_plate = "BEE4R2P"  # TODO: Mocked value
    is_valid = distancia_ponderada(mocked_plate, plate_info["plate"])


    return {"valid": is_valid}


@router.post("/upload")
async def upload_plate_image(request: Request):
    """
    Receives a raw image (JPEG/PNG) and saves it as a PNG file in the uploads directory.
    """
    try:
        data = await request.body()
        image = Image.open(io.BytesIO(data))

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"uploads/camera_{timestamp}.png"
        image.save(filename, format="PNG")

        return {"filename": filename}

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format or unreadable file."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the image."
        )
