from typing import List
import time


def now(return_float=False):
    """
    Get time now (UNIX timestamp)
    :return: timestamp
    """
    time_now = time.time()
    return time_now if return_float else int(time_now)


def diff_list(in_list: List, not_in_list: List) -> List:
    """
    This function gets all elment in `in_list` without not in `not_in_list`
    :param in_list: (list)
    :param not_in_list: (list)
    :return:
    """
    return [x for x in in_list if x not in not_in_list]
