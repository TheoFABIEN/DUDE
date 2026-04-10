from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import zipfile
import os
import tempfile
from PIL import Image
import base64
from io import BytesIO
from torch import cuda, serialization

from FlatbugDetection import load_model, load_model_cpu, predict, predict_cpu
from BioclipClassification import load_classifier, classify_boxes


OUTPUT_DIR = "/tmp/jobs"
os.makedirs(OUTPUT_DIR, exist_ok = True)

app = FastAPI(title="DetectoClassif Backend - Flatbug Only")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")

DEVICE = "cuda:0"

@app.on_event("startup")
async def startup():
    print("Loading models...")
    load_model(DEVICE)
    print("Model 1/3 loaded")
    load_model_cpu()
    print("Model 2/3 loaded")
    load_classifier()
    print("Model 3/3 loaded")
    print("READY")


def crop_to_base64(img, box):
    x1, y1, x2, y2 = box
    crop = img.crop((x1, y1, x2, y2))
    buffered = BytesIO()
    crop.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

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

        results = []
        job_id = tempfile.gettempprefix()
        for i, fname in enumerate(os.listdir(tmpdir)):
            fpath = os.path.join(tmpdir, fname)
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                img = Image.open(fpath).convert("RGB")
                img_filename = f"img_{i}.jpg"
                img_path = os.path.join(OUTPUT_DIR, img_filename)
                img.save(img_path, "JPEG")
                cuda.empty_cache()
                try:
                    pred = predict(img)
                except cuda.OutOfMemoryError:
                    cuda.empty_cache()
                    pred = predict_cpu(img)
                boxes = pred["boxes"]
                classes = classify_boxes(img, boxes)

                objects = []
                for j, (box, cls) in enumerate(zip(boxes, classes)):
                    crop_filename = f"crop_{i}_{j}.jpg"
                    x1, y1, x2, y2 = box
                    img.crop((x1, y1, x2, y2)).save(os.path.join(OUTPUT_DIR, crop_filename), "JPEG")
                    objects.append({
                        "bbox": box,
                        "crop_url": f"/api/static/{crop_filename}",
                        "pred": cls["pred"],
                        "top_k": cls["top_k"]
                    })
                    print("BOX: ", box)
                    print("CLASS: ", cls)
                results.append({
                    "image_url": f"/api/static/{img_filename}",
                    "objects": objects
                })

        if results == []:
            return {"status": "novalidinput"}

    return {"status": "done", "pred_output": results}


@app.post("/download")
async def download_results(data: dict):
    """
    Returns the results as a .zip file containing JSON text files.
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img in enumerate(data["pred_output"]):
            json_data = {
                "image_index": i,
                "objects": []
            }
            for obj in img["objects"]:
                json_data["objects"].append({
                    "bbox": obj.get("bbox", None),
                    "pred": obj["pred"],
                    "confidence": obj["top_k"][0][1] if obj["top_k"] else None,
                    "top_k": obj["top_k"]
                })
            zf.writestr(f"image_{i}.json", json.dumps(json_data, indent=2))
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=results.zip"}
    )