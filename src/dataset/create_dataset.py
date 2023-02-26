# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:19:34 2023

@author: tom
"""

import random
import numpy as np
import skimage as sk
import json
import os

OUTPUT_DIR = "processed_images_01"

# Limit the number of processed images
IMAGE_LIMIT = 2000
current_image_number = 0

# Size of the image in pixels
image_size = 48
pattern_name = "pattern_(48, 48).png"

"""
Returns the pattern with a random size and translation
It is stored as a grayscale image from [0, 1]. Transparent for values over 1.
"""
pattern_img = sk.io.imread(pattern_name, as_gray=True)
def scale_and_rotate_pattern():
    
    # Rescale pattern
    size = abs(int(np.random.normal(0.3, 0.2) * image_size))
    if abs(size) > image_size:
        size = image_size / 2
    size = max(15, size)
    
    img_rescaled = sk.transform.resize(pattern_img, (size, size), anti_aliasing=True)
    
    # Rotate
    angle = np.random.normal(0, 10)
    print(angle)
    img_rotated = sk.transform.rotate(img_rescaled, angle, False, cval=2, 
                                      mode="reflect")
    
    return img_rotated
    
def paste_pattern(img, pattern, pattern_size, posX, posY):
    for x in range(0, pattern_size):
        for y in range(0, pattern_size):
            if pattern[x, y] > 1: continue
        
            # Weird bug : we need to invert x and y axis... :(
            img[posY + y, posX + x] = pattern[x, y]

    return img

def add_bounding_box(bounding_boxes, name, x, y, size):
    label = "pattern"
    
    parameters = [{
        "label": label,
        "x": x,
        "y": y,
        "width": size,
        "height": size,
    }]
    
    bounding_boxes[name] = parameters
    return bounding_boxes
    

def create_and_save_json(bounding_boxes):
    
    # Basic json data format
    data = {
            "version": 1,
            "type": "bounding-box-labels",
            "boundingBoxes": bounding_boxes
    }

    # Serializing json
    json_object = json.dumps(data, indent=4)
     
    # Writing to sample.json
    with open(OUTPUT_DIR + "/bounding_boxes.labels", "w") as outfile:
        outfile.write(json_object)


def process_image(image_name, image_path, bounding_boxes):
    global current_image_number 
    
    print("Processing image {}".format(current_image_number))
    
    current_image_number += 1
    if current_image_number > IMAGE_LIMIT: return
    
    final_image_name = "pattern__{}".format(image_name)

    # Load the image
    img = sk.io.imread(image_path, as_gray=True)    

    # Get the pattern to the correct size and rotation
    pattern = scale_and_rotate_pattern()
    pattern_size = len(pattern[0])
    
    # Resize it to final image size
    img = sk.transform.resize(img, (image_size, image_size), anti_aliasing=True)
    
    # Put the pattern in the image at a random position
    x = random.randint(0, image_size - pattern_size)
    y = random.randint(0, image_size - pattern_size)
    img = paste_pattern(img, pattern, pattern_size, x, y)
    
    # Add the bounding box
    bounding_boxes = add_bounding_box(bounding_boxes, final_image_name, x, y, 
                                      pattern_size)

    # Save the image
    img_uint = sk.util.img_as_ubyte(img)
    sk.io.imsave("{}/{}".format(OUTPUT_DIR, final_image_name), img_uint)

def process_images_inside_directory(path, bounding_boxes):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(path, file)
            process_image(file, file_path, bounding_boxes)
            
            if current_image_number > IMAGE_LIMIT: return

if __name__ == "__main__":    
    # Create an empty dictionnary to store bounding boxes
    bounding_boxes = {}
    
    # Navigate through the files and process images
    image_root = "Images"
    for root, dirs, files in os.walk(image_root):
        for directory in dirs:
            path = os.path.join(image_root, directory)
            process_images_inside_directory(path, bounding_boxes)
            
            if current_image_number > IMAGE_LIMIT: break
    
    # Save the labels
    create_and_save_json(bounding_boxes)