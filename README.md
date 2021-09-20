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
