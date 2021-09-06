NUM=60

for ((ITERATION=0; ITERATION<=NUM; ITERATION++));
do
    # CONFIG GENERATION
    python configTraj/yamlGen.py $NUM $ITERATION
    # DATA GENERATION
    python run.py configTraj/$ITERATION.yaml examples/resources/scene.obj testData/temp

    file=0.hdf5
    echo $file
    newfile=`echo $file | sed "s/0/$ITERATION/g"`
    echo $newfile


    mv ./testData/temp/$file ./testData/output2/$newfile

done