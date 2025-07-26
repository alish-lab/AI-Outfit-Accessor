import os
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# --- Utility: Extract color histogram (normalized) ---
def extract_color_histogram(image_path):
    image = Image.open(image_path).resize((100, 100)).convert('RGB')
    hist = image.histogram()
    hist = np.array(hist) / np.sum(hist)
    return hist

def extract_aspect_ratio(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return width / height

# --- Get best match using cosine similarity ---
def find_best_match(base_dir, gender, target_category, uploaded_image_path):
    """
    Find the most similar image in the opposite category (e.g., bottoms for upper upload).
    Returns the path to the most similar image.
    """
    target_dir = os.path.join(base_dir, gender, target_category)
    if not os.path.exists(target_dir):
        return None

    uploaded_hist = extract_color_histogram(uploaded_image_path)
    uploaded_aspect = extract_aspect_ratio(uploaded_image_path)
    best_score = -1
    best_match_path = None

    for filename in os.listdir(target_dir):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        img_path = os.path.join(target_dir, filename)
        try:
            target_hist = extract_color_histogram(img_path)
            target_aspect = extract_aspect_ratio(img_path)
            color_sim = cosine_similarity([uploaded_hist], [target_hist])[0][0]
            aspect_sim = 1 - abs(uploaded_aspect - target_aspect) / max(uploaded_aspect, target_aspect, 1e-5)
            # Weighted sum: color is more important, but aspect ratio helps
            similarity = 0.8 * color_sim + 0.2 * aspect_sim
            if similarity > best_score:
                best_score = similarity
                best_match_path = img_path
        except:
            continue

    return best_match_path
