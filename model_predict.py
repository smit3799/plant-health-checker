import tensorflow as tf
import numpy as np
import json
import os
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. LOAD DISEASE MODEL
model_path = os.path.join(BASE_DIR, "plant_health_model.keras")
try:
    model = tf.keras.models.load_model(model_path)
    print("✅ Custom Disease Model Loaded.")
except Exception as e:
    print(f"❌ Error loading disease model: {e}")
    model = None

# Load class names
json_path = os.path.join(BASE_DIR, "class_names.json")
try:
    with open(json_path, "r") as f:
        class_names = json.load(f)
        print(f"✅ Loaded {len(class_names)} Class Names.")
except Exception as e:
    print(f"❌ Error loading class names: {e}")
    class_names = []

# 2. LOAD GATEKEEPER
print("⏳ Loading Plant Validator...")
validator_model = MobileNetV2(weights='imagenet')
print("✅ Plant Validator Loaded.")

IMG_SIZE = (224, 224)


def check_if_plant(image_path):
    try:
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        preds = validator_model.predict(img_array)
        decoded = decode_predictions(preds, top=3)[0]

        plant_keywords = [
            'plant', 'leaf', 'flower', 'fruit', 'vegetable', 'tree', 'grass',
            'garden', 'pot', 'greenhouse', 'agriculture', 'orchard', 'forest',
            'corn', 'ear', 'maize', 'apple', 'orange', 'lemon', 'banana',
            'pomegranate', 'strawberry', 'grape', 'cherry', 'peach', 'fig',
            'pineapple', 'pepper', 'cucumber', 'zucchini', 'broccoli', 'cabbage',
            'cauliflower', 'potato', 'mushroom', 'fungus', 'hay', 'straw', 'velvet',
            'nematode', 'slug', 'snail', 'background', 'tissue', 'pattern'
        ]

        top_prediction = decoded[0][1]
        for _, label, score in decoded:
            if any(keyword in label.lower() for keyword in plant_keywords):
                return True, label
        return False, top_prediction
    except Exception as e:
        print(f"Validator Error: {e}")
        return True, "Error"


def predict_image(image_path):
    if model is None:
        return "Model Error", 0.0

    # 1. Load Image
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img)

    # --- DEBUGGING STEP ---
    print(f"DEBUG: Max pixel value BEFORE division: {np.max(img_array)}")

    # 2. Normalize (Divide by 255.0)
    # img_array = img_array / 255.0

    # --- DEBUGGING STEP ---
    print(f"DEBUG: Max pixel value AFTER division: {np.max(img_array)}")
    # The value here MUST be 1.0. If it is 255, the math is failing.

    img_array = np.expand_dims(img_array, axis=0)

    # 3. Predict
    prediction = model.predict(img_array)

    # Print the top 3 guesses to see if the model is confused
    top_3_indices = np.argsort(prediction[0])[-3:][::-1]
    print("--- Model Top 3 Guesses ---")
    for i in top_3_indices:
        print(f"{class_names[i]}: {prediction[0][i] * 100:.2f}%")
    print("---------------------------")

    class_index = np.argmax(prediction)
    confidence = float(np.max(prediction)) * 100

    return class_names[class_index], confidence
