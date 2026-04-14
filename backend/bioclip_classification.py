"""
Functions to handle bounding boxes classification using Bioclip2.
"""

from bioclip import TreeOfLifeClassifier, Rank


def load_classifier(device):
    """
    Loads the classifier model.
    """
    return TreeOfLifeClassifier(device=device)


def bboxes_to_pil(img, boxes):
    """
    Extracts bounding boxes as PIL images from the base image.
    Inputs:
        - img (PIL image): base image.
        - bboxes (list): list of N lists, each one associated with a bounding
          box, with format [x1, y1, x2, y2].
    Returns:
        pil_boxes(list): List of N PIL images.
    """
    pil_boxes = []
    for box in boxes:
        x1, y1, x2, y2 = box
        pil_box = img.crop((x1, y1, x2, y2))
        pil_boxes.append(pil_box)

    return pil_boxes


def predict_boxes_classes(pil_boxes, classifier, top_k = 5):
    """
    BioClip2 classification for each bounding box
    Inputs:
        - boxes(list): list of cropped bounding boxes in PIL format.
    Returns:
        - list of dict
    """
    output = []
    all_predictions = classifier.predict(
        pil_boxes,
        rank = Rank.SPECIES
    )
    for i in range(len(pil_boxes)):
        preds = all_predictions[i * top_k : (i + 1) * top_k]
        topk = [
            (p["species"], float(p["score"]))
            for p in preds
        ]
        best_class = topk[0][0] if topk else None
        output.append({
            "pred": best_class,
            "top_k": topk
        })
    return output


def classify_boxes(img, boxes, classifier):
    """
    Quality of life function
    """
    pil_boxes = bboxes_to_pil(img, boxes)
    return predict_boxes_classes(pil_boxes, classifier)
