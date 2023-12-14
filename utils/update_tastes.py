import random
import pandas as pd
from collections import Counter


def generate_tastes(restaurant_df: pd.DataFrame = None, mock=True):
    """

    :param info:
    :param mock:
    :return:
    """
    # info will be a dictionary that store the restaurant info of the current pool.
    if mock:
        tastes = ['taste '+str(random.randint(0, 100)) for _ in range(14)]
    else:
        # retrieve all category tags for all these restaurants
        x = list(restaurant_df['category tags'])

        # flatten the list
        y = [a for sublist in x for a in sublist]

        # count the tags
        # OK, now look at the occurance of these category tags
        word_counts = Counter(y)
        ranked_words = word_counts.most_common()
        tastes = [r[0] for r in ranked_words]

    return tastes
