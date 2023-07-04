#Imports
from PIL import Image
from random import randrange

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        if self.crop_type == 'center':
        #    return self.center_crop(image, self.shape)
            width, height = image.size
            new_height, new_width = self.shape

            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = (width + new_width) / 2
            bottom = (height + new_height) / 2

            return image.crop((left, top, right, bottom))

        elif self.crop_type == 'random':
        #    return self.random_crop(image, self.shape)

            width, height = image.size
            new_height, new_width = self.shape

            left = randrange(0, width - new_width)
            top = randrange(0, height - new_height)
            right = left + new_width
            bottom = top + new_height

            return image.crop((left, top, right, bottom))
            
        else:
            raise ValueError('Invalid crop type')
        
        