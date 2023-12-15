import random
import pandas as pd
from collections import Counter


def generate_tastes(restaurant_df: pd.DataFrame = None, mock=True,
                    existing_taste_votes = None,
                    initial_search = True):
    """

    :param info:
    :param mock:
    :return:
    """
    # info will be a dictionary that store the restaurant info of the current pool.
    if mock:
        tags = ['taste '+str(random.randint(0, 100)) for _ in range(14)]
    else:
        if initial_search:
            # retrieve all category tags for all these restaurants
            x = list(restaurant_df['category tags'])

            # flatten the list
            y = [a for sublist in x for a in sublist]

            # count the tags
            # OK, now look at the occurance of these category tags
            word_counts = Counter(y)
            ranked_words = word_counts.most_common()
            tags = [r[0] for r in ranked_words]
        else:
            # update the taste tags with the given initial tastes, votes.

            # take top 4 existing votes
            top_four_keys = sorted(existing_taste_votes, key=existing_taste_votes.get, reverse=True)[:4]
            # take 5 most common dishes from the current pool
            x = list(restaurant_df['10 tags for food categories'])
            y = [a for sublist in x for a in sublist]
            word_counts = Counter(y)
            ranked_words = word_counts.most_common()
            tags = top_four_keys + [r[0] for r in ranked_words]

            # recalculate votes ( as cumulative votes)

    return tags
