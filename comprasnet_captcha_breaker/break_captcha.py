import time
import numpy as np
import cv2
from selenium import webdriver
from comprasnet_captcha_breaker.clipboard import copy_image_to_clipboard, load_image_from_clipboard
from comprasnet_captcha_breaker.prediction import predict_captcha_type, predict_letters


def solve_and_submit(browser, model_list, labels_list):
    """ Solves CAPTCHA and submits solution
    
    :param browser: a Selenium webdriver instance
    :param model_list: list of 5 Keras Sequential models
    :param labels_list: list of 5 LabelBinarizer objects
    """
    # Locating image, copying it to clipboard, and loading into python session
    img_elem = browser.find_element_by_xpath(
            '//*[@id="form1"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/span/img')
    webdriver.ActionChains(browser).context_click(img_elem).perform()
    time.sleep(0.1)
    copy_image_to_clipboard()
    copied_img = load_image_from_clipboard()
    
    # Converting to grayscale and thresholding
    captcha = cv2.cvtColor(np.array(copied_img), cv2.COLOR_RGB2GRAY)
    captcha = cv2.threshold(captcha, 0, 255, cv2.THRESH_BINARY_INV)[1]
    
    # Predicting captcha type
    predicted_class = predict_captcha_type(captcha,
                                               model=model_list[0],
                                               labels=labels_list[0])
    
    # Predicting solution
    if predicted_class == 'dotted_wave':
        captcha_text = 'ERROR'
    else:
        captcha_text = predict_letters(captcha, predicted_class,
                                           model_list, labels_list)
    
    # Submitting captcha solution
    browser.find_element_by_id(id_ = 'idLetra').send_keys(captcha_text)
    browser.find_element_by_id(id_ = 'idSubmit').click()
    time.sleep(0.2)


def break_captcha(browser, html_source: str,
                  model_list, labels_list,
                  max_attempts=20):
    """ Loops in a CAPTCHA page until it is solved
    
    :param browser: a Selenium webdriver instance
    :param html_source: source of the html page containing the CAPTCHA
    :param model_list: list of 5 Keras Sequential models
    :param labels_list: list of 5 LabelBinarizer objects
    :return: new html_source
    """
    attempts = 0
    while '<title>Comprasnet' in html_source and attempts < max_attempts:
        solve_and_submit(browser, model_list, labels_list)
        html_source = browser.page_source
        attempts += 1

    if attempts == max_attempts:
        return('max_attempts')
    else:
        return(html_source)