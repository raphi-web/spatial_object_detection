import os
from shutil import copyfile
from collections import Counter
import csv

outpath = "outputs/"

print("\n")
print("*"*40)
print("Enter a name for the project:")
proj = input("project name: ")
test_frac = float(input("test-sample fraction: "))

print("*"*40)
os.makedirs(outpath + proj)
outpath += proj + "/"

os.makedirs(outpath + "cfg")
os.makedirs(outpath + "images")
os.makedirs(outpath + "labels")
os.makedirs(outpath + "backup")

img_labels = [i.split(".")[0] for i in os.listdir("inputs")]
counts = dict(Counter(img_labels))

count_set = set(list(counts.values()))

if 1 in count_set:
    print("Warning, some Imges do not have matching label files or vise versa!")


pairs = []
for key,value in counts.items():
    if value > 1:
        pairs.append(key)
 	
images = [i + ".jpg" for i in pairs]
labels = [i + ".txt" for i in pairs]
 		

for image_file in images:
    copyfile("inputs/" + image_file, outpath + "images/" + image_file)


classes = []
for label_file in labels:
    with open( "inputs/" + label_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        file_classes = [row[0] for row in reader]

        classes +=  file_classes

unique_classes = set(classes)


#  Generate Names File
print("1) Generating generic '.names' file")

f = open(f"{outpath}{proj}.names", "w")
for i in unique_classes:
    f.write(f"class_{i}\n")
f.close()


#  Save Labels Files
print("2) Saving Label Files")
for label_file in labels:
    copyfile("inputs/" + label_file, outpath + "labels/"+ label_file)


#  Train & Test.txt
print("3) Writing train.txt & test.txt")

if len(images) == 1:
    train_images = images
    test_images = images

elif len(images) ==2:
    train_images = [images[0]]
    test_images = [images[1]]

else:
   
    numb_imgs = len(images)
    idx = int(numb_imgs * test_frac)

    train_images = images[:-1 * idx]
    test_images = images[-1 * idx:]
 

f = open(f"{outpath}train.txt", "w")
for image_file in train_images:
    f.write(proj + "/images/" + image_file + "\n")
f.close()


f = open(f"{outpath}test.txt", "w")
for image_file in test_images:
    f.write(proj + "/images/" + image_file+"\n")
f.close()


# Copy Weights 
print("4) copying starting-weights")
copyfile("static_data/darknet53.conv.74", outpath + "darknet53.conv.74")

#  Edit Config File
print("5) Modify configuration file")
file = open("static_data/yolov3-custom.cfg")
cfg_file = file.read()

file.close()

number_of_filter = (len(unique_classes) +5) * 3

cfg_file = cfg_file.replace("$filters$",str(number_of_filter))
cfg_file = cfg_file.replace("$classes$", str(len(unique_classes)))

f = open(outpath + "cfg/" + "yolov3-custom.cfg", "w")
f.write(cfg_file)
f.close()


#  Write .data file
print("6) Writing .data file")
f = open(outpath + "detector.data", "w" )
f.write(f"classes={str(len(unique_classes))}\n")
f.write(f"train={proj}/train.txt\n")
f.write(f"test={proj}/test.txt\n")
f.write(f"names={proj}/{proj}.names\n")
f.write(f"backup={proj}/backup")


# Print commandline string
start = "./darknet detector"
data = f"train {proj}/detector.data"
cfg = f"{proj}/cfg/yolov3-custom.cfg"
weight = f"{proj}/darknet53.conv.74"
print("*" * 60)
print("*" * 60)
print("Finished, copy to darknet foler and run:")
print(f"{start} {data} {cfg} {weight}")
print("*" * 60)
print("*" * 60)
