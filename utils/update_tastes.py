import random


def generate_tastes(restaurant_ids: list = None, mock=True):
    """

    :param info:
    :param mock:
    :return:
    """
    # info will be a dictionary that store the restaurant info of the current pool.
    if mock:
        tastes = ['taste '+str(random.randint(0, 100)) for _ in range(10)]
    else:
        pass

    return tastes
