import io
import os
from tkinter import Tk
from PIL import Image


def copy_image_to_clipboard(sleep_between_keystrokes=(0.2, 0.1, 0.1, 0.7)):
    """Copies the image of a web page using the context menu
    
    Notes:
        1) The context menu must be opened before the function is called;
        2) The command simulates 4 keystrokes in the active window;
        3) The current implementation does not work on Windows.
    
    :param sleep_between_keystrokes: tuple with sleep time between keystrokes, in seconds
    """
    
    command = \
    "xte " + \
    f"'key Down' 'sleep {sleep_between_keystrokes[0]}' " + \
    f"'key Down' 'sleep {sleep_between_keystrokes[1]}' " + \
    f"'key Down' 'sleep {sleep_between_keystrokes[2]}' " + \
    f"'key Return' 'sleep {sleep_between_keystrokes[3]}' "
    
    os.system(command)


def load_image_from_clipboard() :
    """ Loads image stored in the clipboard into python
    
    :return: image as a PIL object
    """
    r = Tk()
    r.withdraw()
    clip = r.clipboard_get(type="image/png")
    r.update()
    r.destroy()
    # Convert hexdump to bytes
    clip = bytes([eval(h) for h in clip.strip().split(' ')])
    cf = io.BytesIO(clip)
    cim = Image.open(cf)
    return(cim)


def save_image_from_clipboard(path) :
    "Saves PNG image stored in the clipboard to provided path"
    r = Tk()
    r.withdraw()
    clip = r.clipboard_get(type="image/png")
    r.update()
    r.destroy()
    # Convert hexdump to bytes
    clip = bytes([eval(h) for h in clip.strip().split(' ')])
    with open(path, mode="bw+") as f:
        f.write(clip)