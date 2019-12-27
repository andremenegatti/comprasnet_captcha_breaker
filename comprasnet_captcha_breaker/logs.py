from typing import List

def read_log_file(txt_file: str, sep=';') -> List[str]:
    """ Reads txt file with scraping logs
    
    :param txt_file: path of a txt file
    :param sep: separator character used to split entries
    :return: list
    """
    with open(txt_file, 'r') as f:
        log_file = [int(x) for x in f.read().split(sep)]
        
    return(log_file)

def save_log(log, path, sep=';'):
    """ Save a log list or integer as a txt file
    
    :param log: a list or an integer
    :param path: output file path, txt format
    :param sep: separator character used between entries
    """
    with open(path, 'w') as f:
        if type(log) == int:
            f.write(str(log))
        else:
            f.write(sep.join(str(x) for x in log))