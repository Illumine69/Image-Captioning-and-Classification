#Imports
from my_package.model import ImageCaptioningModel
from my_package.data import Dataset, Download
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
import numpy as np
from PIL import Image


def experiment(annotation_file, captioner, transforms, outputs):
    '''
        Function to perform the desired experiments

        Arguments:
        annotation_file: Path to annotation file
        captioner: The image captioner
        transforms: List of transformation classes
        outputs: Path of the output folder to store the images
    '''

    #Create the instances of the dataset, download
    dataset = Dataset(annotation_file, transforms)
    download = Download()

    #Print image names and their captions from annotation file using dataset object
    
    for i in range(dataset.__len__()):
        print(dataset.__getann__(i)["file_name"])
        for j in range(len(dataset.__getann__(i)["captions"])):
            print(dataset.__getann__(i)["captions"][j]["caption"])
        print('\n')
    
    #Download images to ./data/imgs/ folder using download object
    
    for i in range(dataset.__len__()):
        download(['./data/imgs/',dataset.__getann__(i)["file_name"]],dataset.__getann__(i)["url"])
    
    #Transform the required image (roll number mod 10) and save it seperately
    
    roll_no = "21CS10057"
    file_name = dataset.__getann__(int(roll_no[-2:])%10)["file_name"]
    transformed_image = dataset.__transformitem__('./data/imgs/'+file_name)
    transformed_image.save('./data/imgs/'+'sample_transformed_'+file_name)
    
    #Get the predictions from the captioner for the above saved transformed image  

    number_of_captions = 3
    print(captioner('./data/imgs/'+'sample_transformed_'+file_name, number_of_captions))

def main():
    captioner = ImageCaptioningModel()
    experiment('./data/annotations.jsonl', captioner, [FlipImage(), BlurImage(1)], None) # Sample arguments to call experiment()
    
if __name__ == '__main__':
    main()