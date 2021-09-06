import os
import glob
import json
import pandas as pd

num_parts = 42

for part in range(num_parts):
    print("part:", part)

    df = pd.read_csv('/freespace/local/sl1642/ocrtoc_materials/objects.csv')
    num_objects = df.shape[0]

    with open(f'output{part}/coco_data/coco_annotations.json', 'r') as f:
        ann = json.load(f)

    categories = []
    for i in range(num_objects):
        obj_id = i + 1
        obj_name = df['object'][i]
        supercategory = df['class'][i]
        entry = {'id': obj_id, 'name': obj_name, 'supercategory': supercategory}
        categories.append(entry)
    ann['categories'] = categories

    img_prefix = f'/freespace/local/sl1642/BlenderProc/examples/ocrtoc/output{part}/coco_data'
    for img in ann['images']:
        img['file_name'] = os.path.join(img_prefix, img['file_name'])

    with open(f'output{part}/coco_data/annotations.json', 'w') as f:
        json.dump(ann, f)
