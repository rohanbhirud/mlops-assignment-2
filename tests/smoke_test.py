import time
import requests
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000"
MAX_RETRIES = 5
RETRY_DELAY = 2

def check_health():
    """Check if the API is healthy."""
    for i in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                logger.info("Health check passed!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        logger.warning(f"Health check failed (attempt {i+1}/{MAX_RETRIES}). Retrying in {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)
    
    return False

def test_prediction(image_path, expected_label=None):
    """Send an image for prediction and measure latency."""
    try:
        path = Path(image_path)
        if not path.exists():
            logger.error(f"Image not found: {image_path}")
            return False

        logger.info(f"Testing with image: {image_path}")
        
        mime_type = 'image/jpeg' if path.suffix.lower() in ['.jpg', '.jpeg'] else 'image/png'
        
        with open(path, 'rb') as f:
            files = {'file': (path.name, f, mime_type)}
            
            start_time = time.time()
            response = requests.post(f"{API_URL}/predict", files=files)
            latency = (time.time() - start_time) * 1000  # ms
            
        if response.status_code == 200:
            result = response.json()
            pred_label = result['predicted_label']
            confidence = result['confidence']
            
            logger.info(f"Prediction success! Label: {pred_label}, Confidence: {confidence:.4f}")
            logger.info(f"Latency: {latency:.2f} ms")
            
            if expected_label:
                if pred_label == expected_label:
                    logger.info(f"Prediction matches expected: {expected_label}")
                else:
                    logger.warning(f"Prediction ({pred_label}) does NOT match expected ({expected_label})")
            return True
        else:
            logger.error(f"Prediction failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Prediction request error: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting smoke tests...")
    
    if not check_health():
        logger.error("API never became healthy. Aborting.")
        sys.exit(1)

    # Test Specific Images
    test_files = [
        ("images/Cat.jpg", "Cat"),
        ("images/Dog.jpg", "Dog")
    ]
    
    success = True
    for path, expected in test_files:
        if Path(path).exists():
            if not test_prediction(path, expected):
                success = False
        else:
            logger.warning(f"Skipping {path} (file not found)")
            # Do not fail if file is missing, just skip (unless strict mode needed)
        
    if success:
        logger.info("All smoke tests passed!")
        sys.exit(0)
    else:
        logger.error("Some smoke tests failed.")
        sys.exit(1)
