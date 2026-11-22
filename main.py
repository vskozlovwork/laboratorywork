import os
from pathlib import Path
import cv2
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, Response

app = FastAPI()
folder = Path(__file__).parent / "images"


def get_files():
    fs = []
    for name in os.listdir(folder):
        if name.endswith((".jpg", ".jpeg", ".png")):
            fs.append(folder / name)
    return sorted(fs)


files = get_files()


@app.get("/api/images")
def list_images():
    result = []
    for i, p in enumerate(files, 1):
        result.append({"id": i, "name": p.name})
    return result


@app.get("/api/images/{image_id}")
def get_image(image_id: int):
    return FileResponse(files[image_id - 1])


@app.get("/api/process/{image_id}")
def process(image_id: int):
    image = cv2.imread(str(files[image_id - 1]), cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, png = cv2.imencode(".png", binary)
    return Response(png.tobytes())



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8555)