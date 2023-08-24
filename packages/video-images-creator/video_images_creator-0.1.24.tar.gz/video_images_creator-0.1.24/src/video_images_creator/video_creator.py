import cv2
import numpy as np
import os
from pathlib import Path
import shutil
import secrets
import string
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen

import pkg_resources

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def build(image_file_paths, feature_names):
    ensure_required_directories_existis()
    current_index = 0
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}'
    os.mkdir(directory_name)
    for index in range(len(image_file_paths) - 1):
        if index % 2 == 0:
            current_index = create_right_to_left_movement(image_file_paths[index + 1], image_file_paths[index], current_index, directory_name, feature_names[index], feature_names[index + 1]) 
        else:
            current_index = create_left_to_right_movement(image_file_paths[index], image_file_paths[index + 1], current_index, directory_name, feature_names[index], feature_names[index+1]) 

    run_ffmpeg(directory_name, folder_name) 
    return flush_video_images(directory_name, folder_name)
   



def create_left_to_right_movement(left_image_file_path, right_image_file_path, current_index_, directory_name, left_screen_name, right_screen_name):

    #create images  

    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path

    parent_current_index = current_index_
    left_image = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_{current_index_}.jpg', 400, "", False)
    right_image = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_{current_index_}.jpg', 1330, "", False) 

    left_image_with_name = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', 400, left_screen_name, True)
    right_image_with_name = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', 1330, right_screen_name, True) 




    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    bg_img = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/background.png")





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

    file_name = f'{directory_name}/combined_left_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
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
        
        cv2.imwrite(f'{directory_name}/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    #create 20 copies of imgage without name

    current_index_ = current_index

    file_name =  f'{directory_name}/combined_right_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1

    current_index_ = current_index

    file_name =  f'{directory_name}/combined_right_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

   

   

    return current_index






def create_right_to_left_movement(left_image_file_path, right_image_file_path, current_index_, directory_name, right_screen_name, left_screen_name):
    #create images
    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path

    #images with no feature name
    parent_current_index = current_index_
    left_image = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_{current_index_}.jpg', 400, "", False)
    right_image = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_{current_index_}.jpg', 1330, "", False) 

    #images with feature names
    left_image_with_name = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', 400, left_screen_name, True)
    right_image_with_name = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', 1330, right_screen_name, True) 


    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    bg_img = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/background.png")

    #these are for feature transitions 
    start_point = np.array([1330, 135])  
    end_point = np.array([400, 135])


    obj_width = 310
    obj_height = 650 


    #create 40 copies of image with names
    current_index = current_index_

    file_name =  f'{directory_name}/combined_right_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1



    #create 20 copies of image without names
    current_index_ = current_index
    file_name =  f'{directory_name}/combined_right_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    num_frames = 70 



    temp_current_index = current_index

    for i in range(0,num_frames):
        t = i / float(num_frames)  
        
        # Get current position 
        position = (1 - t) * start_point + t * end_point  
        
        # Create a copy of the background
        img = bg_img.copy()

        # Define object from img2
        box1 = img2[int(start_point[1]):int(start_point[1] + obj_height), int(start_point[0]):int(start_point[0] + obj_width)]
        # Define object from img1
        box2 = img1[int(end_point[1]):int(end_point[1] + obj_height), int(end_point[0]):int(end_point[0] + obj_width)]
        
        # If the transition is at the start, take the object from img2, otherwise take it from img1
        if t <= 0.5:
            transition_obj = box1
        else:
            transition_obj = box2
        
        # Add object to the current image
        img[int(position[1]):int(position[1] + obj_height), int(position[0]):int(position[0] + obj_width)] = transition_obj

        #frame_index = 76 + i + 2 

        frame_index = temp_current_index + i 
        
        cv2.imwrite(f'{directory_name}/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    current_index_ = current_index

    #create 25 copies of imgage without names

    file_name = f'{directory_name}/combined_left_image_{parent_current_index}.jpg'
    for i in range(25): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1



    #create 40 copies of image with names
    current_index_ = current_index

    file_name =  f'{directory_name}/combined_left_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1


    
  
    


   

    return current_index




def build_screen(screen_file, combine_file_name, x_coordinate, sceen_name, text_to_be_added):
    
    # Load the images
    background = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/background.png")

    


    #overlay = cv2.imread(screen_file) 
    overlay = read_image(screen_file)
    mobile = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/mobile_2.png")

    #resise image
    h_o, w_o, _ = overlay.shape
    overlay = cv2.resize(overlay, (int(w_o * 0.72), int(h_o * 0.60)))   
    overlay = overlay[0: 490, 0:400] 


    #mask
    threshold = 10
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.inRange(mobile[:, :, :3], (0, 0, 0), (threshold, threshold, threshold))
    eroded_mask = cv2.erode(mask, kernel, iterations=1)
    dilated_eroded_mask = cv2.dilate(eroded_mask, kernel, iterations=1) 
    #cv2.imshow('Mask', mask)
    contours, _ = cv2.findContours(dilated_eroded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  

    
    largest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    refined_mask = np.zeros_like(mask)
    cv2.drawContours(refined_mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
    refined_alpha_channel = refined_mask / 255.0
    

    h_o, w_o, _ = overlay.shape
    m_h_o, m_w_o, _ = mobile.shape[:3] 
    h_b, w_b, _ = background.shape 
    x, y = x_coordinate + 20, 210 
    m_x, m_y = x_coordinate, 135


    #background[m_y:m_y+m_h_o, m_x: m_x+m_w_o] = mobile 
    background = alpha_blend(mobile[:, :, :3], background, refined_alpha_channel, m_x, m_y)
    background[y:y+h_o, x:x+w_o] = overlay 


    # if text_to_be_added == True:
    #     font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    #     font_scale = 2
    #     font_thickness = 3
    #     text = sceen_name
    #     (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    #     if x_coordinate == 400:
    #         x = x_coordinate + 350
    #     else:
    #         x = x_coordinate - 400  
    #     y = background.shape[0] - 540  

    #     cv2.putText(background, text, (x, y), font, font_scale, (255, 255, 255), font_thickness, lineType=cv2.LINE_AA)  


    ## ----- Apply white color ----- ######## 
    # Define a mask for black color
    # Here we are assuming that any pixel with RGB values (0,0,0) is black.
    # You can change the thresholds if you need to catch near-black colors.
    lower = np.array([0, 0, 0], dtype="uint8")
    upper = np.array([1, 1, 1], dtype="uint8")
    mask = cv2.inRange(background, lower, upper)

    # Change black to white
    background[mask == 255] = [255, 255, 255]


    

    # Save the modified image

    if text_to_be_added:
        # Convert OpenCV image to Pillow format
        pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))

        # Load the custom font
        font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')

        
        font_size = 47
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)

        text = sceen_name
        if x_coordinate == 400:
            x = x_coordinate + 350
        else:
            x = x_coordinate - 400  
        y = background.shape[0] - 540  

        draw.text((x, y), text, font=font, fill=(255, 255, 255))

        # Convert Pillow image back to OpenCV format
        background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


    cv2.imwrite(combine_file_name, background)

    return combine_file_name


def alpha_blend(foreground, background, alpha, x, y):
    """
    Perform alpha blending.
    
    Parameters:
    - foreground: The top image.
    - background: The image where the top image will be overlaid.
    - alpha: The transparency mask.
    - x, y: The coordinates to overlay the top image.
    
    Returns:
    - Blended image.
    """
    h, w, _ = foreground.shape
    blended = background.copy()
    for c in range(3):
        blended[y:y+h, x:x+w, c] = (foreground[:, :, c] * alpha + blended[y:y+h, x:x+w, c] * (1 - alpha))
    return blended 

def run_ffmpeg(directory_name, uniq_code):
    os.system(f"source ~/.bash_profile && ffmpeg -y -framerate 60 -i {directory_name}/frame_%d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p -r 60 outputs/output_{uniq_code}.mp4")  
    

def flush_video_images(diretory_name, folder_name):
    try:
        # Use shutil.rmtree() to remove the entire folder and its contents
        shutil.rmtree(diretory_name)
        #print(f"Folder '{diretory_name}' and its contents have been deleted.")
        return f"outputs/output_{folder_name}.mp4"
    except Exception as e:
        #print(f"An error occurred: {e}")
        return f"outputs/output_{folder_name}.mp4"

def read_image(image_url):
    resp = urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) # The image object
    return image 

def ensure_required_directories_existis():
    if not os.path.exists("images"):
        try:
            os.mkdir("images") 
        except Exception as e:
            print("Exception occured", e) 
    if not os.path.exists("outputs"):
        try:
            os.mkdir("outputs")
        except Exception as e:
            print("Exception occured..", e)


if __name__ == "__main__":
    image_file_paths = ["video_images_creator/features/launch.png", "video_images_creator/features/first.png","video_images_creator/features/second.png", "video_images_creator/features/third.png", "video_images_creator/features/fourth.png", "video_images_creator/features/fifth.png"] 
    feature_names = ["Splash Screen", "Search", "Dashboard", "Settings", "Profile/Bio", "Analytics" ]
    #image_file_paths = ["video_images_creator/features/launch.png", "video_images_creator/features/first.png", "video_images_creator/features/second.png"]

    build(image_file_paths, feature_names) 


