from io import BytesIO
import requests as rq
from PIL import Image
import time


def scrape_captchas(save_path: str, n: int, url_source='default'):
    """ Download multiple CAPTCHAs as png files
    
    Note: if 'url_source' is not provided, the following will be used:
        "http://comprasnet.gov.br/scripts/srf/intercepta/captcha.aspx?opt=image"
    
    :param save_path: directory where png files will be stored
    :param n: number of CAPTCHAs to download
    :param url_source: CAPTCHA-generator URL
    """
    if url_source == 'default':
        url_source = "http://comprasnet.gov.br/scripts/srf/intercepta/captcha.aspx?opt=image"

    error_index_list = [0, 0]
    
    for i in range(1, n + 1):
        print("Downloading captcha no. " + str(i))
        try:
            response = rq.get(url_source)
            im = Image.open(BytesIO(response.content)).convert("RGB")
            im.save(save_path + f"/{str(i).zfill(6)}.png")
        except:
            print("Error!")
            if error_index_list[-1] != 0:
                error_index_list.append(i)
                i = i - 1
                time.sleep(5)
                continue
            elif i == error_index_list[-1] == error_index_list[-2]:
                error_index_list.append(i)
                break
            else:
                error_index_list.append(i)
                i = i - 1
                time.sleep(5)
                continue




def get_captcha(url_source='default'):
    """ Loads a single CAPTCHA into python session 
    
    Note: if 'url_source' is not provided, the following will be used:
        "http://comprasnet.gov.br/scripts/srf/intercepta/captcha.aspx?opt=image"
    
    :param url_source: CAPTCHA-generator URL
    """
    if url_source == 'default':
        url_source = "http://comprasnet.gov.br/scripts/srf/intercepta/captcha.aspx?opt=image"
    
    response = rq.get(url_source)
    im = Image.open(BytesIO(response.content)).convert("RGB")
    
    return (im)