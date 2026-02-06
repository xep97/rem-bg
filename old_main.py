from rembg import remove
from PIL import Image
import os

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

user_input = input(
    "Enter image paths or folder paths (comma-separated): "
)

paths = [p.strip() for p in user_input.split(",") if p.strip()]


image_files = []

for path in paths:
    if os.path.isdir(path):
        # Add all images in folder
        for file in os.listdir(path):
            if file.lower().endswith(IMAGE_EXTENSIONS):
                image_files.append(os.path.join(path, file))

    elif os.path.isfile(path) and path.lower().endswith(IMAGE_EXTENSIONS):
        image_files.append(path)

    else:
        print(f"Skipping invalid path: {path}")

if not image_files:
    print("No valid images found.")
    exit()


output_dir = "new_photos"
os.makedirs(output_dir, exist_ok=True)

index = 1
while os.path.exists(os.path.join(output_dir, f"photo{index}.png")):
    index += 1

for img_path in image_files:
    try:
        input_image = Image.open(img_path)
        output_image = remove(input_image)

        output_path = os.path.join(output_dir, f"photo{index}.png")
        output_image.save(output_path)

        print(f"Saved: {output_path}")
        index += 1

    except Exception as e:
        print(f"Failed to process {img_path}: {e}")

print(f"Done! Processed {index - 1} image(s).")
