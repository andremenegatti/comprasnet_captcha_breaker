from typing import List

def check_consec_errors(int_list: List[int], n: int) -> bool:

    if len(int_list) < n:
        return(False)
    else:
        if int_list[-1] == (int_list[-n] + (n - 1)):
            return(True)
        else:
            return(False)