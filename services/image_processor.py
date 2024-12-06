from PIL import Image
from io import BytesIO
import base64

class ImageProcessor:
  @staticmethod
  async def process_image(image_data: bytes) -> str:
    img = Image.open(BytesIO(image_data))
    img.thumbnail((800, 800))
        
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode()