from flat_bug.predictor import Predictor
from torchvision.transforms.functional import pil_to_tensor

model = None

def load_model(device):
    global model
    if model is None:
        model = Predictor(device=device)

def predict(image):
    return model(
        pil_to_tensor(image)
    ).json_data