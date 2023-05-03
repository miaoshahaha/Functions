import os 
import shutil

def split_data(name: str,
               split_data: float=0.8):
    
    # Create a directory for the images.
    image_name = name
    src_dir = Path(f'{image_name}/')
    dst_train_dir = Path(f'data/train/{image_name}')
    dst_test_dir = Path(f'data/test/{image_name}')
    
    if not (dst_train_dir.is_dir() and dst_test_dir.is_dir()):
        print("----------Creating a train-test-split directory.----------")
        dst_train_dir.mkdir(parents=True, exist_ok=True)
        dst_test_dir.mkdir(parents=True, exist_ok=True)
        
    # Split the data by parameters provided
    split = int(len(os.listdir(src_dir)) * split_data) 

    
    # Load the images to the directory.
    for train_image in os.listdir(src_dir)[:split]:
        train_path = os.path.join(src_dir, train_image)
        dst_train_path = os.path.join(dst_train_dir)

        shutil.copy(train_path, dst_train_path)
        
    for test_image in os.listdir(src_dir)[split:]:
        test_path = os.path.join(src_dir, test_image)
        dst_test_path = os.path.join(dst_test_dir)

        shutil.copy(test_path, dst_test_path)
        
    print("Splitting complete. ")
    print(f"Number of training data : {int(len(os.listdir(dst_train_dir)))}")
    print(f"Number of testing data : {int(len(os.listdir(dst_test_dir)))}")
        
# Select the images to be splitted here.
split_data(u'英梨梨')