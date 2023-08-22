import cv2
import numpy as np
import os
from pathlib import Path
import shutil
from build_screen import build_screen




def create_left_to_right_movement(left_image_file_path, right_image_file_path, current_index_, left_screen_name, right_screen_name):

    #create images  

    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path

    parent_current_index = current_index_
    left_image = build_screen(left_image_file_name, f'combined_left_image_${current_index_}.jpg', 400, "", False)
    right_image = build_screen(right_image_file_name, f'combined_right_image${current_index_}.jpg', 1330, "", False) 

    left_image_with_name = build_screen(left_image_file_name, f'combined_left_image_with_name${current_index_}.jpg', 400, left_screen_name, True)
    right_image_with_name = build_screen(right_image_file_name, f'combined_right_image_with_name${current_index_}.jpg', 1330, right_screen_name, True) 




    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    bg_img = cv2.imread('background.png')





    #these are for feature transitions 
    start_point = np.array([400, 135])  
    end_point = np.array([1330, 135])   


    obj_width = 310
    obj_height = 650 


    #  #create 40 copies of image with names
    # current_index = current_index_

    # file_name =  f'combined_left_image_with_name${parent_current_index}.jpg'
    # for i in range(40): 
    #     index = i + current_index_
    #     destination = f'./images/frame_{index}.jpg'
    #     shutil.copyfile(file_name, destination)
    #     current_index = current_index + 1



    #create 20 copies of image without names
    current_index = current_index_

    #create 20 copies of img1

    file_name = f'combined_left_image_${parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'./images/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    num_frames = 70 



    temp_current_index = current_index

    for i in range(num_frames):
        t = i / float(num_frames)  

        
        position = (1 - t) * start_point + t * end_point  

        
        img = bg_img.copy()

        
        box1 = img1[int(start_point[1]):int(start_point[1] + obj_height), int(start_point[0]):int(start_point[0] + obj_width)]
        box2 = img2[int(end_point[1]):int(end_point[1] + obj_height), int(end_point[0]):int(end_point[0] + obj_width)]

        
        transition_obj = (1 - t) * box1 + t * box2

        
        img[int(position[1]):int(position[1] + obj_height), int(position[0]):int(position[0] + obj_width)] = transition_obj

        #frame_index = 76 + i + 2 

        frame_index = temp_current_index + i 
        
        cv2.imwrite(f'./images/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    #create 20 copies of imgage without name

    current_index_ = current_index

    file_name =  f'combined_right_image${parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'./images/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1

    current_index_ = current_index

    file_name =  f'combined_right_image_with_name${parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'./images/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

   

   

    return current_index

