"""Image handling and prediction helpers for the saved binary classifier."""
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

CLASS_NAMES = ("Counterfeit", "Original")  # Sorted directory class order at training.

def preprocess_image(image: Image.Image, size=(224, 224)) -> np.ndarray:
    image = ImageOps.exif_transpose(image).convert("RGB")
    image = image.resize(size, resample=Image.Resampling.BILINEAR)
    return np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)

def decode_prediction(prob_original: float, threshold: float = 0.5):
    probability = float(prob_original)
    if not np.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("The model returned an invalid probability.")
    is_original = probability >= threshold
    return {"label": CLASS_NAMES[int(is_original)], "score": probability if is_original else 1 - probability,
            "original_probability": probability}
