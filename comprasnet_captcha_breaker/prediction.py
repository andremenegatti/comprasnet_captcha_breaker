import numpy as np
from comprasnet_captcha_breaker.resize_to_fit import resize_to_fit
from comprasnet_captcha_breaker.segmentation import split_captcha


def predict_captcha_type(captcha, model, labels):
    """ Predicts CAPTCHA type using a CNN
    
    Identified types: Bubble, BubbleCut, Dotted, DottedWave, Wave
    
    :param captcha: thresholded captcha as a 90x200 numpy.ndarray
    :param model: Keras Sequential model
    :param labels: LabelBinarizer
    :return: a string indicating the CAPTCHA type
    """
    # Expanding array dimensions to match Keras' expectations
    captcha = np.expand_dims(captcha, axis = 2)
    captcha = np.expand_dims(captcha, axis = 0)
    
    # Predicting captcha type
    class_prediction = model.predict(captcha)
    predicted_class = labels.inverse_transform(class_prediction)[0]
    
    return(predicted_class)
    





def predict_letters_single_model(captcha, captcha_class, model, labels,
                                 letter_width, letter_height):
    
    """ Solves the CAPTCHA using the supplied CNN.
    
    :param captcha: thresholded captcha as a 90x200 numpy.ndarray
    :param captcha_class: a string indicating the CAPTCHA type
    :param model: Keras Sequential model
    :param labels: LabelBinarizer
    :param letter_width: width of letter images, as expected by the CNN
    :param letter_height: height of letter images, as expected by the CNN
    :return: a string with the solution (hopefully)
    """
    output = split_captcha(captcha, captcha_class = captcha_class)
    
    if output == 'error':
        return('ERROR')
    
    predictions = []
    
    for image in output:
        # Adding additional padding to make images of same size
        image = resize_to_fit(image, letter_width, letter_height)
        # Adding a third channel dimension to the image (Keras expects this)
        image = np.expand_dims(image, axis=2)
        image = np.expand_dims(image, axis=0)
        # Asking the neural network to make a prediction
        prediction = model.predict(image)
        # Converting the one-hot-encoded prediction back to a normal letter
        predicted_letter = labels.inverse_transform(prediction)[0]
        predictions.append(predicted_letter)
    
    # Returning the captcha's text
    captcha_text = "".join(predictions)
    return(captcha_text)




def predict_letters(captcha,
                    captcha_class,
                    model_list,
                    labels_list,
                    param_dict={
                            'Wave': {'index': 1, 'size': 60},
                            'Dotted': {'index': 2, 'size': 60},
                            'Bubble': {'index': 3, 'size': 86},
                            'BubbleCut': {'index': 4, 'size': 85}
                            }
                    ):
    """ Solves the CAPTCHA using appropriate CNN from supplied list
    
    :param captcha: thresholded captcha as a 90x200 numpy.ndarray
    :param model_list: list of 5 Keras Sequential models
    :param labels_list: list of 5 LabelBinarizer objects
    :param param_dict: dictionary with the index and letter dimensions for each model
    :return: a string with the CAPTCHA solution (hopefully)
    """
    
    index = param_dict[captcha_class]['index']
    size = param_dict[captcha_class]['size']
    
    captcha_text = predict_letters_single_model(captcha, captcha_class,
                                                model=model_list[index],
                                                labels=labels_list[index],
                                                letter_width=size,
                                                letter_height=size)
    
    return(captcha_text)
    
    
    
    
    
    
    
    