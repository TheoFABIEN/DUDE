from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import os
import tempfile
from PIL import Image
import base64
from io import BytesIO
from torch import cuda, serialization

from FlatbugDetection import load_model, load_model_cpu, predict, predict_cpu
#from BioclipClassification import load_classifier, classify_boxes

app = FastAPI(title="DetectoClassif Backend - Flatbug Only")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

DEVICE = "cuda:0"


load_model(DEVICE)
load_model_cpu()

@app.post("/upload")
async def upload_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "Only zip file format is accepted"})

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        images_output = []
        for fname in os.listdir(tmpdir):
            fpath = os.path.join(tmpdir, fname)
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                img = Image.open(fpath).convert("RGB")
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                cuda.empty_cache()
                try:
                    pred = predict(img)
                except cuda.OutOfMemoryError:
                    cuda.empty_cache()
                    pred = predict_cpu(img)
                boxes = pred["boxes"]
                #classes = classify_boxes(img, boxes)
                images_output.append({
                    "image": img_base64,
                    "boxes": pred["boxes"]
                })

        if images_output == []:
            return {"status": "novalidinput"}

    return {"status": "done", "images_output": images_output}