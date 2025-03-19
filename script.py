import os
from PIL import Image
import shutil

labels_dir = "labels"
images_dir = "images"
output_dir = "sorted_dataset"

os.makedirs(output_dir, exist_ok=True)

train_ration = 0.8
val_ration = 0.1
test_ration = 0.1
bad_labels_count = 0

labels = [f for f in os.listdir(labels_dir) if f.endswith(".txt")]

def check_label(txt):
    label_path = os.path.join(labels_dir, txt)
    seen = set()
    try:
        with open(label_path, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) == 5:
                    cls, x, y ,w ,h = map(float, parts)
                    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                        return True
                    if line in seen:
                        return True
                    else:
                        seen.add(line)
                else:
                    return True
    except Exception as e:
        print(f"Label read error {e}")
        return True

def check_and_save(labels_to_save, dir):
    bad_images_count = 0
    output_images = os.path.join(output_dir, dir, "images")
    output_labels = os.path.join(output_dir, dir , "labels")
    os.makedirs(output_labels, exist_ok=True)
    os.makedirs(output_images, exist_ok=True)
    images = [f.replace(".txt", ".jpg") for f in labels_to_save]
    for image in images:
        image_path = os.path.join(images_dir, image)
        try:
            with Image.open(image_path) as f:
                f.save(os.path.join(output_images,image))
            shutil.copy(os.path.join(labels_dir, image.replace(".jpg", ".txt")), os.path.join(output_labels, image.replace(".jpg",".txt")))
        except Exception as e:
            print(f"Read error {e}")
            bad_images_count += 1
            print(image_path)

    if bad_images_count != 0:
        print(f"Пропущено изображений:{bad_images_count}")

for label in labels[:]:
    if check_label(label):
        labels.remove(label)
        bad_labels_count += 1

print(f"Удаленно неправильных файлов разметки: {bad_labels_count}")

train_count = int(len(labels) * train_ration)
val_count = int(len(labels) * val_ration)
test_count = int(len(labels) * test_ration)

train_labels = labels[:train_count]
val_labels = labels[train_count:train_count + val_count]
test_labels = labels[train_count + val_count:]

check_and_save(train_labels, "train")
check_and_save(val_labels, "val")
check_and_save(test_labels, "test")

print(f"train: {train_count}, val: {val_count}, test: {test_count}")