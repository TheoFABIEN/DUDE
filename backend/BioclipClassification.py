from bioclip import TreeOfLifeClassifier, Rank
from PIL import Image

classifier = None
TOP_K = 5 # keep top 5 predictions

def load_classifier():
    global classifier
    if classifier is None:
        classifier = TreeOfLifeClassifier()


def bboxesToPIL(img, boxes):
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


def classifyBoxes(pil_boxes):
    """
    BioClip2 classification for each bounding box
    Inputs:
        - boxes(list): list of cropped bounding boxes in PIL format.
    Returns:
        - list
    """
    result = classifier.predict(pil_boxes)
    output = []
    for r in result:
        topk = [
            (r.label[i], float(r.prob[i])) 
            for i in range(min(TOP_K, len(r.label)))
        ]
        best_class = topk[0][0] if topk else None
        output.append({"pred": best_class, "top_k": topk})
    return output


def classify_boxes(img, boxes):
    pil_boxes = bboxesToPIL(img, boxes)
    return classifyBoxes(pil_boxes)
