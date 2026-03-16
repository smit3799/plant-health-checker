import tensorflow as tf
import os
import zipfile

# ---------------------------------------------------------
# 1. AUTO-EXTRACTION (Makes it work on Professor's PC)
# ---------------------------------------------------------
ZIP_FILENAME = "PlantVillage.zip"
EXTRACT_FOLDER = "data_cache"  # We extract into this folder

# Check if the zip file actually exists in the project folder
if not os.path.exists(ZIP_FILENAME):
    print(f"ERROR: '{ZIP_FILENAME}' not found!")
    print("   Please put the PlantVillage.zip file in the same folder as this script.")
    raise FileNotFoundError("Zip file missing.")

# Extract only if we haven't already (saves time on 2nd run)
if not os.path.exists(EXTRACT_FOLDER):
    print(f"Extracting {ZIP_FILENAME}... (This may take a moment)")
    with zipfile.ZipFile(ZIP_FILENAME, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)
    print("Extraction Complete!")
else:
    print("Data already extracted. Using existing folder.")

# ---------------------------------------------------------
# 2. DEFINE PATHS (Relative Paths = Portable)
# ---------------------------------------------------------
# PlantVillage zip usually contains a folder named 'PlantVillage' inside
dataset_dir = os.path.join(EXTRACT_FOLDER, "PlantVillage")

# If the zip structure is different (e.g. direct files), adjust this:
if not os.path.exists(dataset_dir):
    # Fallback: maybe the zip extracted directly to data_cache?
    dataset_dir = EXTRACT_FOLDER

train_dir_path = os.path.join(dataset_dir, "train")
val_dir_path = os.path.join(dataset_dir, "val")

# Safety Check
if not os.path.exists(train_dir_path):
    print(f"CRITICAL ERROR: Could not find 'train' folder at: {train_dir_path}")
    print("   Check your zip file structure.")
    raise FileNotFoundError("Train folder missing.")

# ---------------------------------------------------------
# 3. LOAD DATASETS
# ---------------------------------------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

print("Loading Training Data...")
train_ds_raw = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir_path,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
    seed=123
)

print("Loading Validation Data...")
val_ds_raw = tf.keras.preprocessing.image_dataset_from_directory(
    val_dir_path,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
    seed=123
)

# Use Validation as Test set
test_ds_raw = val_ds_raw

# ---------------------------------------------------------
# 4. NORMALIZE & OPTIMIZE
# ---------------------------------------------------------
AUTOTUNE = tf.data.AUTOTUNE

# IMPORTANT: Normalizing to 0-1 range (x / 255.0)
# You MUST update model_predict.py to match this!
def preprocess(image, label):
    return image / 255.0, label

print("Optimizing Datasets...")

# .cache() is removed to prevent crashing RAM on laptops
train_ds = train_ds_raw.map(preprocess).shuffle(200).prefetch(AUTOTUNE)
val_ds = val_ds_raw.map(preprocess).prefetch(AUTOTUNE)
test_ds = test_ds_raw.map(preprocess).prefetch(AUTOTUNE)

class_names = train_ds_raw.class_names
print(f"Success! Found {len(class_names)} classes.")

# Export for other files
__all__ = ["train_ds", "val_ds", "test_ds", "IMG_SIZE", "class_names"]
