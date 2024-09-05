import os
import random
import cv2
import sys
import shutil

origin_data_folder = "./origin_data"
images_folder = "./datasets/yolo/images"
labels_folder = "./datasets/yolo/labels"
if os.path.exists(images_folder):
    shutil.rmtree(images_folder)
os.mkdir(images_folder)
if os.path.exists(labels_folder):
    shutil.rmtree(labels_folder)
os.mkdir(labels_folder)

fishing_float_data = []

for folder in os.listdir(origin_data_folder):
    mark_file = os.path.join(origin_data_folder, folder, "mark.csv")
    if os.path.exists(mark_file):
        with open(mark_file, "r") as f:
            _in = False
            for line in f:
                [img_path, id, x, y, w, h] = line.strip().split(",")
                if int(id) == 1:
                    _in = True
                    fishing_float_data.append(
                        (img_path, int(id), int(x), int(y), int(w), int(h))
                    )
                elif _in:
                    break

random.shuffle(fishing_float_data)
rand_index = int(len(fishing_float_data) * 0.8)
train_data = fishing_float_data[:rand_index]
val_data = fishing_float_data[rand_index:]

os.mkdir(os.path.join(images_folder, "train"))
os.mkdir(os.path.join(labels_folder, "train"))
totle = len(train_data)
for i, data in enumerate(train_data):
    img_path, id, x, y, w, h = data
    img = cv2.imread(img_path)
    height, width, channel = img.shape
    new_img_path = os.path.join(images_folder, "train", f"fishing_float-train-{i}.jpg")
    shutil.copy(img_path, new_img_path)
    label_path = os.path.join(labels_folder, "train", f"fishing_float-train-{i}.txt")
    with open(label_path, "w") as f:
        f.write(f"{id-1} {x / width} {y / height} {w / width} {h / height}")
    sys.stdout.write(f"\rtrain data:[{i+1}/{totle}]")
    sys.stdout.flush()
print()

os.mkdir(os.path.join(images_folder, "val"))
os.mkdir(os.path.join(labels_folder, "val"))
totle = len(val_data)
for i, data in enumerate(val_data):
    img_path, id, x, y, w, h = data
    new_img_path = os.path.join(images_folder, "val", f"fishing_float-val-{i}.jpg")
    label_path = os.path.join(labels_folder, "val", f"fishing_float-val-{i}.txt")
    img = cv2.imread(img_path)
    height, width, channel = img.shape
    # cv2.imwrite(new_name + ".jpg", img)
    shutil.copy(img_path, new_img_path)
    with open(label_path, "w") as f:
        f.write(f"{id-1} {x / width} {y / height} {w / width} {h / height}")
    sys.stdout.write(f"\rval data:[{i+1}/{len(val_data)}]")
    sys.stdout.flush()
print()
