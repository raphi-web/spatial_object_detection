import cv2
import numpy as np
import os

CONF_THRESH, NMS_THRESH = 0.5, 0.5

config = "krater_mkiii/cfg/yolov3-custom.cfg"
weights = "krater_mkiii/backup/yolov3-custom_final.weights"


def read_img(image,config,weights):
   
    net = cv2.dnn.readNetFromDarknet(config, weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Read and convert the image to blob and perform forward pass to get the bounding boxes with their confidence scores
    img = cv2.imread(image)
    height, width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    class_ids, confidences, b_boxes = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONF_THRESH:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                x = int(center_x - w / 2) # <----------------------------------
                y = int(center_y - h / 2)

                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    return class_ids, confidences,b_boxes


f = open("results.txt","w")

for image_file in ["to_test/" + i for i in os.listdir("to_test/") if i.split(".")[-1] == "jpg"]:
    class_ids, conf,bbox = read_img(image_file,config,weights)
    
    for class_id,conf,(x,y,w,h) in zip(class_ids, conf,bbox):
        img = image_file.split("/")[-1]

        f.write(f"{img}, {class_id}, {conf}, {x}, {y}, {w}, {h}\n")

f.close()
       
    
