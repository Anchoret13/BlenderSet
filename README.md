# USAGE

```
python camPoseGen.py NUMBER CAMERA_HEIGHT RADIUS
bash ./run.sh
```


Then run following command (Change the path to your own path)
```
mkdir coco_single_object
mkdir coco_single_object/coco_data
mkdir mask
mkdir mask/coco_data

cp /home/dyf/dataset/test.py /home/dyf/dataset/ocrtoc_video_test/0001/coco_data
cp /home/dyf/dataset/renameColor.py /home/dyf/dataset/ocrtoc_video_test/0001/coco_data

cd /home/dyf/dataset/ocrtoc_video_test/0001

mkdir annotations

mv /home/dyf/dataset/ocrtoc_video_test/0001/mask/coco_data /home/dyf/dataset/ocrtoc_video_test/0001/annotations
mv /home/dyf/dataset/ocrtoc_video_test/0001/bop_data/OCRTOC/camera.json /home/dyf/dataset/ocrtoc_video_test/0001/
mv /home/dyf/dataset/ocrtoc_video_test/0001/bop_data/OCRTOC/train_pbr/000000/depth /home/dyf/dataset/ocrtoc_video_test/0001/

cp /home/dyf/dataset/renameMask.py /home/dyf/dataset/ocrtoc_video_test/0001/annotations/coco_data
cd /home/dyf/dataset/ocrtoc_video_test/0001/annotations/coco_data
python renameMask.py
```
then rename anotations/coco_data to annotations/masks, delete non-essential files, and rename generated video 0001

USE for loop to generate videos, don't forget to rename video


### Selected Objects
a_cups,
bleach_cleanser,
bowl,
cracker_box,
cup_small,
d_cups,
doraemon_bowl,
doraemon_cup,
e_cups,
foam_brick,
gleatin_box,
hello_kitty_cup,
hello_kitty_plate,
large_clamp,
medium_clamp,
mustrad_bottle,
pan_tefal,
pepsi,
potted_meat_can,
power_drill,
pudding_box,
realsense_box,
redbull,
rubiks_cube,
sugar_box,
tea_can1,
tomato_soup_can,
tuna_fish_can,
wood_block,
wooden_puzzle1
