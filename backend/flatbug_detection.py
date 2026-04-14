"""
Functions to handle object detection using Flatbug.
"""


from flat_bug.predictor import Predictor
from torchvision.transforms.functional import pil_to_tensor


def load_model(device):
    """Load model with chosen device"""
    return Predictor(device=device)

def load_model_cpu():
    """Load model with cpu"""
    return Predictor(device='cpu')

def predict(image, model):
    """Predict on single PIL image"""
    return model(
        pil_to_tensor(image)
    ).json_data

def predict_cpu(image, model_cpu):
    """Predict on single PIL image using CPU"""
    return model_cpu(
        pil_to_tensor(image)
    ).json_data
