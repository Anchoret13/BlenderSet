#!/bin/bash

#export CUDA_VISIBLE_DEVICES=$1
#echo "CUDA_VISIBLE_DEVICES=$1"

REPOSITORY="/home/dyf/Desktop/robo/BlenderProc"
CONFIG="${REPOSITORY}/examples/ocrtoc/config.yaml"
OUTPUT="/home/dyf/dataset/ocrtoc_video"
DATASET="/home/dyf/dataset/ocrtoc"
CAMERA_CONFIG="${REPOSITORY}/examples/ocrtoc/camera.json"
CC_MATERIALS="${REPOSITORY}/resources/cctextures/"

COUNT=1
while [  $COUNT -lt 2 ]; do

    VIDEO=$(printf "%04d" $COUNT)
    printf "Start generating video: " $VIDEO

    python run.py $CONFIG $OUTPUT/$VIDEO $DATASET $CAMERA_CONFIG $CC_MATERIALS "/home/dyf/Desktop/robo/BlenderProc/camPose"

    let COUNT=COUNT+1
done
