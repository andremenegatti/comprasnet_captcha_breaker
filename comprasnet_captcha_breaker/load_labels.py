import pickle

def load_labels(label_filename):
    """ Loads pickled LabelBinarizer object
    
    :param label_filename: path of a .dat file
    return: a LabelBinarizer object
    """
    with open(label_filename, 'rb') as f:
        lb = pickle.load(f)
        return(lb)