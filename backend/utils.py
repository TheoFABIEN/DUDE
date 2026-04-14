"""
Helper functions used in main.py.
"""

import os
import zipfile
import json
from io import BytesIO
from PIL import Image
from torch import cuda

from fastapi.responses import StreamingResponse
from flatbug_detection import predict, predict_cpu
from bioclip_classification import classify_boxes



def process_single_image(fpath, fname, i, job_path, job_id, state):
    """ Helper to process an individual image """
    img = Image.open(fpath).convert("RGB")
    img_filename = f"img_{i}.jpg"
    img.save(os.path.join(job_path, img_filename), "JPEG")

    #####   OBJECT DETECTION   #####
    cuda.empty_cache()
    try:
        pred = predict(img, state.detector)
    except cuda.OutOfMemoryError:
        cuda.empty_cache()
        pred = predict_cpu(img, state.detector_cpu)

    #####   CLASSIFICATION   #####
    boxes = pred["boxes"]
    objects = []
    for j, (box, cls) in enumerate(
        zip(
            boxes,
            classify_boxes(img, boxes, state.classifier)
        )
    ):
        crop_name = f"crop_{i}_{j}.jpg"
        img.crop(box).save(os.path.join(job_path, crop_name), "JPEG")
        objects.append({
            "bbox": box,
            "crop_url": f"/api/static/{job_id}/{crop_name}",
            "pred": cls["pred"],
            "top_k": cls["top_k"]
        })

    return {
        "image_name": fname,
        "image_width": img.size[0],
        "image_height": img.size[1],
        "image_url": f"/api/static/{job_id}/{img_filename}",
        "objects": objects
    }


def generate_default(data: dict):
    """
    Generates inference results using the default file format.
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for img in data["pred_output"]:
            image_name = img.get("image_name", "unknown.jpg")
            base_name = os.path.splitext(os.path.basename(image_name))[0]
            json_filename = f"{base_name}.json"
            json_data = {
                "image_name": image_name,
                "objects": []
            }
            for obj in img["objects"]:
                json_data["objects"].append({
                    "bbox": obj.get("bbox", None),
                    "pred": obj["pred"],
                    "confidence": obj["top_k"][0][1] if obj["top_k"] else None,
                    "top_k": obj["top_k"]
                })
            zf.writestr(json_filename, json.dumps(json_data, indent=2))
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=results.zip"}
    )


def create_coco_box_annotation(ann_id, img_id, obj, cat_id):
    """
    Calculates bbox dimensions and returns a COCO annotation dict.
    Used inside generate_coco().
    """
    x1, y1, x2, y2 = obj["bbox"]
    width, height = x2 - x1, y2 - y1
    return {
        "id": ann_id,
        "image_id": img_id,
        "category_id": cat_id,
        "bbox": [x1, y1, width, height],
        "area": width * height,
        "iscrowd": 0
    }

def generate_coco(data: dict):
    """
    Generates inference results using the COCO 1.0 file format.
    """
    buffer = BytesIO()
    images = []
    annotations = []
    categories = {}
    ann_id = 1
    cat_id = 1

    for i, img in enumerate(data["pred_output"], start=1):
        images.append({
            "id": i,
            "file_name": img.get("image_name", f"img_{i}.jpg"),
            "height": img["image_height"],
            "width": img["image_width"]
        })
        for obj in img["objects"]:
            label = obj["pred"]
            if label not in categories:
                categories[label] = cat_id
                cat_id += 1

            annotations.append({create_coco_box_annotation(
                ann_id,
                i,
                obj,
                categories[label]
            )})
            ann_id += 1

    coco_content = {
        "images": images,
        "annotations": annotations,
        "categories": [
            {"id": v, "name": k}
            for k, v in categories.items()
        ]
    }

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("annotations.json", json.dumps(coco_content, indent=2))

    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/zip")
