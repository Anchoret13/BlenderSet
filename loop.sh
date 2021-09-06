for i in {0..50}
do
    python scripts/saveAsImg.py examples/advanced/object_pose_sampling/output/$i.hdf5
done

find -type f -name '*_distance.png' -delete
find -type f -name '*_normals.png' -delete