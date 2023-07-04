#Imports
from my_package.model import ImageCaptioningModel
from my_package.data import Dataset, Download
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
import numpy as np
from PIL import Image
import os

'''
Transform image with multiple transformations and printing captions using ImageCaptionModel()
'''
## The transformed images are stored in ./data/imgs/output folder
#Dictionary to save image number to aid in image naming according to the problem statement
transforms_num = 9  #Number of transforms
image_name = []
num = 0
for i in range(transforms_num):
    image_name.append(chr(i + ord('a')))

def experiment(annotation_file, captioner, transforms, outputs):
    '''
        Function to perform the desired experiments

        Arguments:
        annotation_file: Path to annotation file
        captioner: The image captioner
        transforms: List of transformation classes
        outputs: Path of the output folder to store the images
    '''
    global num
    #Create the instances of the dataset, download
    dataset = Dataset(annotation_file, transforms)
    download = Download()

    #Transform the required image (roll number mod 10) and save it seperately
    
    if os.path.exists(outputs) is False:
        os.mkdir(outputs)

    roll_no = "21CS10057"
    file_name = dataset.__getann__(int(roll_no[-2:])%10)["file_name"]
    transformed_image = dataset.__transformitem__('./data/imgs/' + file_name)
    transformed_image.save(outputs+image_name[num]+'_'+file_name)

    #Get the predictions from the captioner for the above saved transformed image  

    number_of_captions = 3
    print(captioner(outputs+image_name[num]+'_'+file_name, number_of_captions))
    num = num + 1 # Incrementing the image name number

def main():
 
    #Using Image Caption Model to generate 3 captions for various transformations
    captioner = ImageCaptioningModel()
    path = './data/imgs/output/'
    #The original image(a_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [], path)
    #Horizontally flipped original image(b_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [FlipImage()], path)
    #Blurred image (with some degree of blurring)(c_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [BlurImage(2)], path)
    #Twice Rescaled image (2X scaled)(d_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [RescaleImage(427*2)], path) #default image size is (640,427)
    #Half Rescaled image (0.5X scaled)(e_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [RescaleImage((640/2,427/2))], path)
    #90 degree right rotated image(f_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [RotateImage(-90)], path)
    #45 degree left rotated image(g_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [RotateImage(45)], path)

    ##Some more transformations

    #center cropped image(h_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [CropImage([300,300], 'center')], path)
    #random cropped image(i_7.jpg)
    experiment('./data/annotations.jsonl', captioner, [CropImage([300,300], 'random')], path)

if __name__ == '__main__':
    main()