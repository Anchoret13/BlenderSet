import json
from pycocotools.coco import COCO
import os, sys, zipfile
import urllib.request
import shutil
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import os

json_file = './coco_annotations.json'
data=json.load(open(json_file,'r'))

for i in range(1000):
    data_2 = {}
    data_2['info'] = data['info']
    data_2['licenses'] = data['licenses']
    data_2['images'] = [data['images'][i]]
    data_2['categories'] = data['categories']
    annotation = []
 
    imgID = data_2['images'][0]['id']
    for ann in data['annotations']:
        if ann['image_id'] == imgID:
            annotation.append(ann)
 
    data_2['annotations'] = annotation
    img_file=data_2['images'][0]['file_name']
    img_first=img_file.split(".")[0]
    
    json.dump(data_2, open('../coco_single_object/'+img_first+'.json', 'w'), indent=4)

json_path = "../coco_single_object/coco_data"
img_path = "../"
color_img_save = "../color"
binary_img_save = "../binary"

#get_single_binaryImg(json_path,img_path,color_img_save,binary_img_save)

def get_single_maskID(json_path,img_path,color_img_save,mask_img_save):
    dir=os.listdir(json_path)
    for jfile in dir:
        annFile =os.path.join(json_path,jfile)
        coco = COCO(annFile)
        imgIds = coco.getImgIds()
        img = coco.loadImgs(imgIds[0])[0]
        dataDir = img_path
        shutil.copy(os.path.join(dataDir, img['file_name']), color_img_save)

        catIds = coco.getCatIds()
        for ann in coco.dataset['annotations']:
            if ann['image_id'] == imgIds[0]:
                catIds.append(ann['category_id'])

        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
        width = img['width']
        height = img['height']
        anns = coco.loadAnns(annIds)
        mask = np.zeros((480,640))
        
        for i, ann in enumerate(anns):
            mask_tmp = coco.annToMask(ann)
            # mask_tmp[mask_tmp > 0] = i + 1
            #plt.imshow(mask_tmp)
            mask[mask_tmp > 0] = ann['category_id']
        
        # mask = coco.annToMask(anns[7])
        
        # for i in range(len(anns)):
        #     mask += coco.annToMask(anns[i])
        
        #print(mask)
        #plt.imshow(mask)
        #plt.show()

        imgs = np.zeros(shape=(height, width, 3), dtype=np.float32)
        imgs[:, :, 0] = mask[:, :]
        imgs[:, :, 1] = mask[:, :]
        imgs[:, :, 2] = mask[:, :]
        imgs = imgs.astype(int)
        img_name = img['file_name'].split(".")[0]
        imgs = imgs.astype(np.uint8)
        plt.imsave(mask_img_save + "/" + img_name + ".png", imgs)

mask_img_save = "../mask"

get_single_maskID(json_path,img_path,color_img_save,mask_img_save)