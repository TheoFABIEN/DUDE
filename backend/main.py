import time
import json
import zipfile
import os
import shutil
import uuid
import tempfile
from PIL import Image
from io import BytesIO
from torch import cuda
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from FlatbugDetection import load_model, load_model_cpu, predict, predict_cpu
from BioclipClassification import load_classifier, classify_boxes


DEVICE = "cuda:0"
READY = False
OUTPUT_DIR = "/tmp/jobs"
MAX_AGE_SECONDS = 18000     # life time for stored files
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


def cleanup_old_jobs():
    """
    Deletes files older than MAX_AGE_SECONDS
    """
    now = time.time()
    if not os.path.exists(OUTPUT_DIR):
        return

    for item in os.listdir(OUTPUT_DIR):
        item_path = os.path.join(OUTPUT_DIR, item)
        if os.stat(item_path).st_mtime < now - MAX_AGE_SECONDS:
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                print(f"GC: Cleaning of {item_path} done.")
            except Exception as e:
                print(f"GC: Error while cleaning {item_path}: {e}")


@app.on_event("startup")
async def startup():
    global READY
    print("Loading models...")
    load_model(DEVICE)
    load_model_cpu()
    load_classifier()
    READY = True
    print("READY")


@app.get("/health")
def health():
    if READY:
        return {"status": "ready"}
    return JSONResponse(status_code=503, content={"status": {"loading"}})


@app.post("/upload")
async def upload_zip(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    background_tasks.add_task(cleanup_old_jobs)

    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "Only zip file format is accepted"})

    job_id = str(uuid.uuid4())
    job_path = os.path.join(OUTPUT_DIR, job_id)
    os.makedirs(job_path, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        results = []
        for i, fname in enumerate(os.listdir(tmpdir)):
            fpath = os.path.join(tmpdir, fname)
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                img = Image.open(fpath).convert("RGB")
                img_filename = f"img_{i}.jpg"
                img_save_path = os.path.join(job_path, img_filename)
                img.save(img_save_path, "JPEG")
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
                    crop_save_path = os.path.join(job_path, crop_filename)
                    x1, y1, x2, y2 = box
                    img.crop((x1, y1, x2, y2)).save(crop_save_path, "JPEG")
                    objects.append({
                        "bbox": box,
                        "crop_url": f"/api/static/{job_id}/{crop_filename}",
                        "pred": cls["pred"],
                        "top_k": cls["top_k"]
                    })
                    print("BOX: ", box)
                    print("CLASS: ", cls)
                results.append({
                    "image_url": f"/api/static/{job_id}/{img_filename}",
                    "objects": objects
                })

        if not results:
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
