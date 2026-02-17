import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from src.api import app, preprocess_image, SimpleCNN
import torch
from PIL import Image
import numpy as np

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_preprocess_image():
    # Create a dummy image
    img = Image.new('RGB', (100, 100), color='red')
    img_size = 128
    
    # Process
    tensor = preprocess_image(img, img_size)
    
    # Check shape: (1, 3, 128, 128)
    assert tensor.shape == (1, 3, 128, 128)
    assert isinstance(tensor, torch.Tensor)
