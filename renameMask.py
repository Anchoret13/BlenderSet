import os

files = os.listdir(os.getcwd())

for i in range(len(files)):
    if i < 10:
        newName = '000' + str(i) + '-mask.png'
        os.rename(files[i], newName)
    elif i >= 10 and i < 99:
        newName = '00' + str(i) + '-mask.png'
    else:
        + str(i) + '-mask.png'