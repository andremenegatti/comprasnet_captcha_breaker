from comprasnet_captcha_breaker.split_dotted import split_dotted
from comprasnet_captcha_breaker.split_bubble import split_bubble
from comprasnet_captcha_breaker.split_wave import split_wave

def split_captcha(captcha, captcha_class):
    """ Splits CAPTCHA into a different array for each character
    
    Wrapper around specific functions for each CAPTCHA type
    
    :param captcha: thresholded captcha as a 90x200 numpy.ndarray
    :param captcha_class: a string indicating the CAPTCHA type
    :return: a list of 6 numpy.ndarray objects
    """
    if captcha_class in ['bubble', 'bubble_cut']:
        letters = split_bubble(captcha)
    elif captcha_class == 'wave':
        letters = split_wave(captcha)
    elif captcha_class == 'dotted':
        letters = split_dotted(captcha)
    
    return(letters)