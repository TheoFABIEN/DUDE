"""
Functions to handle object detection using Flatbug.
"""


from flat_bug.predictor import Predictor
from torchvision.transforms.functional import pil_to_tensor

model = None
model_cpu = None

def load_model(device):
    """Load model with chosen device"""
    global model
    if model is None:
        model = Predictor(device=device)

def load_model_cpu():
    """Load model with cpu"""
    global model_cpu
    if model_cpu is None:
        model_cpu = Predictor(device='cpu')

def predict(image):
    """Predict on single PIL image"""
    return model(
        pil_to_tensor(image)
    ).json_data

def predict_cpu(image):
    """Predict on single PIL image using CPU"""
    return model_cpu(
        pil_to_tensor(image)
    ).json_data
