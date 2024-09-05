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

marked_data = []

for folder in os.listdir(origin_data_folder):
    mark_file = os.path.join(origin_data_folder, folder, "mark.csv")
    if os.path.exists(mark_file):
        with open(mark_file, "r") as f:
            _in = False
            count = 0
            for line in f:
                [img_path, id, x, y, w, h] = line.strip().split(",")
                id = int(id)
                if not _in and id == 1:
                    _in = True
                if _in:
                    marked_data.append((img_path, id, int(x), int(y), int(w), int(h)))
                    if id == 2:
                        count += 1
                    if count >= 8:
                        break

random.shuffle(marked_data)
rand_index = int(len(marked_data) * 0.8)
train_data = marked_data[:rand_index]
val_data = marked_data[rand_index:]

os.mkdir(os.path.join(images_folder, "train"))
os.mkdir(os.path.join(labels_folder, "train"))
totle = len(train_data)
for i, data in enumerate(train_data):
    img_path, id, x, y, w, h = data
    if id == 1:
        file_name = "fishing"
    elif id == 2:
        file_name = "fish_bites"
    else:
        continue
    img = cv2.imread(img_path)
    height, width, channel = img.shape
    new_img_path = os.path.join(images_folder, "train", f"{file_name}-train-{i}.jpg")
    label_path = os.path.join(labels_folder, "train", f"{file_name}-train-{i}.txt")
    shutil.copy(img_path, new_img_path)
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
    if id == 1:
        file_name = "fishing"
    elif id == 2:
        file_name = "fish_bites"
    else:
        continue
    new_img_path = os.path.join(images_folder, "val", f"{file_name}-val-{i}.jpg")
    label_path = os.path.join(labels_folder, "val", f"{file_name}-val-{i}.txt")
    img = cv2.imread(img_path)
    height, width, channel = img.shape
    shutil.copy(img_path, new_img_path)
    with open(label_path, "w") as f:
        f.write(f"{id-1} {x / width} {y / height} {w / width} {h / height}")
    sys.stdout.write(f"\rval data:[{i+1}/{len(val_data)}]")
    sys.stdout.flush()
print()
