import numpy as np
import cv2

def split_wave(captcha):
    """ Performs character segmentation in a 'wave' CAPTCHA
    
    :param captcha: thresholded 'dotted' captcha as a 90x200 numpy.ndarray
    :return: a list of 6 numpy.ndarray objects
    """
    thresh = cv2.copyMakeBorder(captcha.copy(), 8, 8, 8, 8, cv2.BORDER_CONSTANT, 0)
    hcontours = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours = hcontours[0]

    conts = [(c,) for c, x in enumerate(hcontours[1][0]) if x[3] == -1]

    for pingij_index, pingij in [(index, cc) for index, cc in enumerate(contours) if (cv2.boundingRect(cc)[3] < 10) and (index, ) in conts]:
        pingij_coordx = max(pingij, key = lambda coords: coords[0][1])[0][0]
        dists = []

        for cont_item in [index[0] for index in conts if len(index) == 1]:
            l = contours[cont_item]
            l_index = cont_item
            if np.array_equal(l, pingij): continue
            dist = abs(pingij_coordx - min(l, key = lambda coords: coords[0][1])[0][0])
            dists.append((dist, l_index))

        try:
            min_index = min(dists)[1]
            conts.remove((min_index,))
            conts.remove((pingij_index,))
            conts.append((pingij_index, min_index))

        except:
            return('error')

    if len(conts) != 6:
        return('error')

    sorted_conts = []
    for i in conts:
        if len(i) == 1:
            (x, y, w, h) = cv2.boundingRect(contours[i[0]])
        else:
            (x_pingij, y_pingij, w_pingij, h_pingij) = cv2.boundingRect(contours[i[0]])
            (x_ij, y_ij, w_ij, h_ij) = cv2.boundingRect(contours[i[1]])
            x = min(x_pingij, x_ij)
            y = y_pingij
            w = max(x_pingij + w_pingij, x_ij + w_ij) - x
            h = y_ij + h_ij - y

        letter = np.zeros((106, 216), np.uint8)

        for cont in i:

            letter = cv2.drawContours(image = letter, contours = contours, contourIdx = cont,
                                             color = 255, thickness = -1,
                                             hierarchy = hcontours[1], maxLevel = 2)

        letter_cut = letter[y-2 : y+h+2, x-2 : x+w+2]

        if letter_cut.shape[0] < 11:
            return('error')

        sorted_conts.append((x, letter_cut))

        try:
            sorted_conts = sorted(sorted_conts)
        except:
            pass

    return([x[1] for x in sorted_conts])