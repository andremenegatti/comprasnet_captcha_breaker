import numpy as np
import math as mt

def split_dotted(captcha):
    """ Performs character segmentation in a 'dotted' CAPTCHA
    
    Wrapper around two more specific functions:
        1) split_dotted_f: for 'dotted' captchas starting with lower case 'f';
        2) split_dotted_general: every other 'dotted' captcha
    
    :param captcha: thresholded 'dotted' captcha as a 90x200 numpy.ndarray
    :return: a list of 6 numpy.ndarray objects
    """
    if f_is_first(captcha):
        letters = split_dotted_f(captcha)
    else:
        letters = split_dotted_general(captcha)

    return(letters)



def f_is_first(captcha):
    """ Check if a CAPTCHA of class 'dotted' starts with lower case 'f'
    
    :param captcha:thresholded 'dotted' captcha as a 90x200 numpy.ndarray
    :return: bool
    """
    
    image = captcha[19:46,]

    col_sum = np.sum(image, axis = 0)
    col_sum_list = list(col_sum)
    
    return(col_sum_list[28:36] == [3570, 3570, 0 , 1020, 1020, 0, 510, 510])



def split_dotted_f(captcha):
    """ Performs character segmentation in a 'dotted' CAPTCHA starting with 'f'
    
    :param captcha: thresholded 'dotted' captcha as a 90x200 numpy.ndarray
    :return: a list of 6 numpy.ndarray objects
    """
    # Cropping captcha so that the first letter (f) is not included
    image = captcha[19:46, 36:]
    
    col_sum = np.sum(image, axis = 0)
    col_sum_list = list(col_sum)

    # Finding all the dark regions
    # beggining and end of all dark regions)
    x = 1
    i = 0
    dark_regions = []
    while i < 164:
        if col_sum_list[i] == 0:
            dark_region_beg = i
            while col_sum_list[i + x] == 0:
                x = x + 1
                if (x + i) > 163:
                    break
            dark_region_end = i + x - 1
            dark_region = (dark_region_beg, dark_region_end)
            dark_regions.append(dark_region)
            i = x + i + 1
            x = 1
        else:
            i = i + 1

    # Identifying leftmost and rightmost dark regions and popping them out of the list
    left_region = dark_regions[0]
    right_region = dark_regions[-1]
    dark_regions.pop(0)
    dark_regions.pop(-1)

    # Sorting dark regions according to their length
    four_regions = sorted(dark_regions, key = lambda x: x[1] - x[0], reverse = True)

    gaps = []
    lines = []
    for i, region in enumerate(four_regions):
        gap = mt.ceil((region[1] - region[0]) / 2)
        if gap == 0:
            continue
        gaps.append(gap)
        lines.append(region[0] + gap)

    # If more than 4 remaining gaps are identified, the problem may be due to split letters
    # Some of the troublesome letters are m, n and h
    # We will try to fix this issue by completing gaps in these letters
    if len(lines) > 4:

        for i in range(len(col_sum_list[:-9])):
            if col_sum_list[i:i+9] == [0, 0, 0, 0, 510, 510, 0, 3060, 3060]:
                captcha[28:30, i+1:i+3] = 255
            if col_sum_list[i:i+9] == [0, 0, 0, 0, 510, 510, 0, 2550, 2550]:
                captcha[31:33, i+1:i+3] = 255
            if col_sum_list[i:i+9] == [0, 3060, 3060, 0, 510, 510, 0, 0, 0, 0]:
                captcha[28:30, i+7:i+9] = 255
            if col_sum_list[i:i+9] == [0, 2550, 2550, 0, 510, 510, 0, 0, 0, 0]:
                captcha[31:33, i+7:i+9] = 255
            if col_sum_list[i:i+9] == [0, 4080, 4080, 0, 0, 0, 0, 510, 510]:
                captcha[31:33, i+4:i+6] = 255

        # Reloading image (based on modified captcha) and redefiding col_sum_list
        image = captcha[19:46, 36:]
        col_sum_list = list(np.sum(image, axis = 0))

        # Finding all the dark regions
        # beggining and end of all dark regions)
        x = 1
        i = 0
        dark_regions = []
        while i < 164:
            if col_sum_list[i] == 0:
                dark_region_beg = i
                while col_sum_list[i + x] == 0:
                    x = x + 1
                    if (x + i) > 163:
                        break
                dark_region_end = i + x - 1
                dark_region = (dark_region_beg, dark_region_end)
                dark_regions.append(dark_region)
                i = x + i + 1
                x = 1
            else:
                i = i + 1

        # Identifying leftmost and rightmost dark regions and popping them out of the list
        left_region = dark_regions[0]
        right_region = dark_regions[-1]
        dark_regions.pop(0)
        dark_regions.pop(-1)

        # Sorting dark regions according to their length
        four_regions = sorted(dark_regions, key = lambda x: x[1] - x[0], reverse = True)

        # Building a list of GAPS (lengths of the dark regions)
        # and LINES that split such gaps in half
        gaps = []
        lines = []
        for i, region in enumerate(four_regions):
            gap = mt.ceil((region[1] - region[0]) / 2)
            if gap == 0:
                continue
            gaps.append(gap)
            lines.append(region[0] + gap)

        # If the errors persists, we move on to next captcha
        if len(lines) > 4:
            return('error')

    # If the algorithm finds less letters than expected (merged letters), we move on to next captcha
    if len(lines) < 4:
        return('error')

    # Defining rightmost and leftmost lines, appending lines list, and sorting
    left_line = 0
    right_line = right_region[0] + 2
    lines.append(left_line)
    lines.append(right_line)
    lines = sorted(lines)

    # Adjusting coordinates to account for deleting first letter
    lines = list(map(lambda x: x + 36, lines))

    # Finding letters x-coordinates (coordinates for initial r are already included)
    letters_xcoords = [(26, 37)]
    for i in range(len(lines)):
        if lines[i] == lines[-1]:
            break
        letter = (lines[i], lines[i + 1])
        letters_xcoords.append(letter)

    # Finding letters in the captcha, using the x-coordinates
    letters = []
    for i, letter in enumerate(letters_xcoords):
        letter_image = captcha[:60, letter[0]:letter[1]]
        letters.append(letter_image)

    return(letters)





def split_dotted_general(captcha):
    """ Performs character segmentation in a 'dotted' CAPTCHA
    
    :param captcha: thresholded 'dotted' captcha as a 90x200 numpy.ndarray
    :return: a list of 6 numpy.ndarray objects
    """
    image = captcha[19:46,]

    col_sum = np.sum(image, axis = 0)
    col_sum_list = list(col_sum)
    # Finding all the dark regions
    # beggining and end of all dark regions)
    x = 1
    i = 0
    dark_regions = []
    while i < 200:
        if col_sum_list[i] == 0:
            dark_region_beg = i
            while col_sum_list[i + x] == 0:
                x = x + 1
                if (x + i) > 199:
                    break
            dark_region_end = i + x - 1
            dark_region = (dark_region_beg, dark_region_end)
            dark_regions.append(dark_region)
            i = x + i + 1
            x = 1
        else:
            i = i + 1

    # Identifying leftmost and rightmost dark regions and popping them out of the list
    left_region = dark_regions[0]
    right_region = dark_regions[-1]
    dark_regions.pop(0)
    dark_regions.pop(-1)

    # Sorting dark regions according to their length
    five_regions = sorted(dark_regions, key = lambda x: x[1] - x[0], reverse = True)

    # Building a list of GAPS (lengths of the dark regions)
    # and LINES that split such gaps in half
    gaps = []
    lines = []
    for i, region in enumerate(five_regions):
        gap = mt.ceil((region[1] - region[0]) / 2)
        if gap == 0:
            continue
        gaps.append(gap)
        lines.append(region[0] + gap)

    # If more than 5 gaps are identified, the problem may be due to split letters
    # Some of the troublesome letters are m, n and h
    # We will try to fix this issue by completing gaps in these letters
    if len(lines) > 5:

        for i in range(len(col_sum_list[:-9])):
            if col_sum_list[i:i+9] == [0, 0, 0, 0, 510, 510, 0, 3060, 3060]:
                captcha[28:30, i+1:i+3] = 255
            if col_sum_list[i:i+9] == [0, 0, 0, 0, 510, 510, 0, 2550, 2550]:
                captcha[31:33, i+1:i+3] = 255
            if col_sum_list[i:i+9] == [0, 3060, 3060, 0, 510, 510, 0, 0, 0, 0]:
                captcha[28:30, i+7:i+9] = 255
            if col_sum_list[i:i+9] == [0, 2550, 2550, 0, 510, 510, 0, 0, 0, 0]:
                captcha[31:33, i+7:i+9] = 255
            if col_sum_list[i:i+9] == [0, 4080, 4080, 0, 0, 0, 0, 510, 510]:
                captcha[31:33, i+4:i+6] = 255

        # Reloading image (based on modified captcha) and redefiding col_sum_list
        image = captcha[19:46, ]
        col_sum_list = list(np.sum(image, axis = 0))

        # Finding all the dark regions
        # beggining and end of all dark regions)
        x = 1
        i = 0
        dark_regions = []
        while i < 200:
            if col_sum_list[i] == 0:
                dark_region_beg = i
                while col_sum_list[i + x] == 0:
                    x = x + 1
                    if (x + i) > 199:
                        break
                dark_region_end = i + x - 1
                dark_region = (dark_region_beg, dark_region_end)
                dark_regions.append(dark_region)
                i = x + i + 1
                x = 1
            else:
                i = i + 1

        # Identifying leftmost and rightmost dark regions and popping them out of the list
        left_region = dark_regions[0]
        right_region = dark_regions[-1]
        dark_regions.pop(0)
        dark_regions.pop(-1)

        # Sorting dark regions according to their length
        five_regions = sorted(dark_regions, key = lambda x: x[1] - x[0], reverse = True)

        # Building a list of GAPS (lengths of the dark regions)
        # and LINES that split such gaps in half
        gaps = []
        lines = []
        for i, region in enumerate(five_regions):
            gap = mt.ceil((region[1] - region[0]) / 2)
            if gap == 0:
                continue
            gaps.append(gap)
            lines.append(region[0] + gap)

        # If the errors persists, we move on to next captcha
        if len(lines) > 5:
            return('error')

    # If the algorithm finds less letters than expected (merged letters), we move on to next captcha
    if len(lines) < 5:
        return('error')

    # Defining rightmost and leftmost lines, appending lines list, and sorting
    left_line = left_region[1] - 2
    right_line = right_region[0] + 2
    lines.append(left_line)
    lines.append(right_line)
    lines = sorted(lines)

    # Finding letters x-coordinates
    letters_xcoords = []
    for i in range(len(lines)):
        if lines[i] == lines[-1]:
            break
        letter = (lines[i], lines[i + 1])
        letters_xcoords.append(letter)

    letters = []
    for i, letter in enumerate(letters_xcoords):
        letter_image = captcha[:60, letter[0]:letter[1]]
        letters.append(letter_image)

    return(letters)