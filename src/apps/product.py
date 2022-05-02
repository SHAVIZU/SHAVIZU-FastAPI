from fastapi import APIRouter, status, Depends

from src import Settings, get_settings
from src.utils.product import crawl_image_by_style_code


router = APIRouter()


@router.post("/image", status_code=status.HTTP_201_CREATED)
async def crawl_product_image(style_code: str, settings: Settings = Depends(get_settings)):
    img_url = crawl_image_by_style_code(style_code=style_code, settings=settings)

    return {
        'img_url': img_url
    }
