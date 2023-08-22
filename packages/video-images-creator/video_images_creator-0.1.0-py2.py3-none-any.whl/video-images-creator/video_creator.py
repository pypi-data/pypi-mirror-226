from moveL2R import create_left_to_right_movement
from moveR2L import create_right_to_left_movement



def build(image_file_paths, feature_names):
    current_index = 0
    for index in range(len(image_file_paths) - 1):
        if index % 2 == 0:
            current_index = create_right_to_left_movement(image_file_paths[index + 1], image_file_paths[index], current_index, feature_names[index], feature_names[index + 1]) 
        else:
            current_index = create_left_to_right_movement(image_file_paths[index], image_file_paths[index + 1], current_index, feature_names[index], feature_names[index+1])


if __name__ == "__main__":
    image_file_paths = ["features/launch.png", "features/first.png","features/second.png", "features/third.png", "features/fourth.png", "features/fifth.png"] 
    feature_names = ["Splash Screen", "Search", "Dashboard", "Settings", "Profile/Bio", "Analytics" ]
    #image_file_paths = ["features/launch.png", "features/first.png", "features/second.png"]

    build(image_file_paths, feature_names)