"""
Main entrypoint for the detection/classification backend.
Handles image detection and classification using Flatbug and Bioclip2, via 
ZIP uploads.
"""

import time
import zipfile
import os
import shutil
import uuid
import tempfile
from torch import cuda
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from flatbug_detection import load_model, load_model_cpu
from bioclip_classification import load_classifier
from utils import process_single_image, generate_coco, generate_default


os.makedirs("/tmp/jobs", exist_ok = True)

app = FastAPI(title="DetectoClassif Backend - Flatbug Only")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="/tmp/jobs"), name="static")


def cleanup_old_jobs(max_age_seconds = 18000, output_dir="/tmp/jobs"):
    """ Deletes files older than max_age_seconds """
    now = time.time()
    if not os.path.exists(output_dir):
        return

    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        if os.stat(item_path).st_mtime < now - max_age_seconds:
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                print(f"GC: Cleaning of {item_path} done.")
            except OSError as e:
                print(f"GC: Error while cleaning {item_path}: {e}")


@app.on_event("startup")
async def startup():
    """ Initializes models and sets application state to ready. """
    print("Loading models...")
    app.state.detector = load_model("cuda:0")
    app.state.detector_cpu = load_model_cpu()
    app.state.classifier = load_classifier(device="cuda" if cuda.is_available else "cpu")

    app.state.ready = True
    print("READY")


@app.get("/health")
def health():
    """ Checks if the models are loaded and the service is ready."""
    if getattr(app.state, "ready", False):
        return {"status": "ready"}
    return JSONResponse(status_code=503, content={"status": "loading"})


@app.post("/upload")
async def upload_zip(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    output_dir="/tmp/jobs"
):
    """Extracts zip, runs inference, and returns detection results."""
    background_tasks.add_task(cleanup_old_jobs)

    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "Only zip file format is accepted"})

    job_id = str(uuid.uuid4())
    job_path = os.path.join(output_dir, job_id)
    os.makedirs(job_path, exist_ok=True)

    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "upload.zip")
        with open(zip_path, "wb") as buffer:
            buffer.write(await file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        for i, fname in enumerate(os.listdir(tmpdir)):
            fpath = os.path.join(tmpdir, fname)
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                img_results = process_single_image(
                    fpath,
                    i,
                    job_path,
                    job_id,
                    app.state
                )
                results.append(img_results)

    if not results:
        return {"status": "novalidinput"}

    return {"status": "done", "pred_output": results}


@app.post("/download")
async def download_results(data: dict):
    """
    Returns the results as a .zip file containing JSON text files.
    """
    format_type = data.get("format", "default")
    if format_type == "coco":
        return generate_coco(data)
    return generate_default(data)
