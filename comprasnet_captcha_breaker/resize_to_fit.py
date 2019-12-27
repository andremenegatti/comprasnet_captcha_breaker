import math as mt
import cv2

def resize_to_fit(image, width: int, height: int):
    """ Adds black padding to an image so it matches a required shape
    
    :param image: thresholded image as a numpy.ndarray
    :param width: required width (not be lower than initial width)
    :param height: required height (not lower than initial height)
    :return: numpy.ndarray of the reshaped image
    """
    shape = image.shape
    left = mt.ceil((width - shape[1])/2)
    right = mt.floor((width - shape[1])/2)
    top = mt.ceil((height - shape[0])/2)
    bottom = mt.floor((height - shape[0])/2)
    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, 0)
    return(image)