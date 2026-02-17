import kagglehub

# Download latest version
path = kagglehub.dataset_download("bhavikjikadara/dog-and-cat-classification-dataset")

print("Path to dataset files:", path)

import shutil
import os

target_dir = "data/dog-and-cat-classification-dataset"
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)

print(f"Moving dataset to {target_dir}...")
shutil.copytree(path, target_dir)
print("Done.")
