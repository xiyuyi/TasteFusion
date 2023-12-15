def calculate_score(votes, tags_list):
    score = 0
    for tag in tags_list:
        score += int(votes.get(tag, 0))  # Add the vote value if tag is in votes, otherwise add 0
    return score


def update_restaurants(taste_votes=None,
                       current_restaurant_df=None,
                       mock=False,
                       d_top_n = -10):
    """
    This function takes inthe current taste_votes and the current pool of restaurants,
    and return a new list of suggested restaurants, and generate new taste tags.

    :param mock:
    :param taste_votes:
    :param current_restaurant_df:
    :return: filtered_restaurants_df
    """

    print('current_taste_votes:')
    for k, v in taste_votes.items():
        print(f"{k}: {v}")
    print(type(current_restaurant_df))
    print(current_restaurant_df.shape)

    # added votes to the column
    current_restaurant_df['votes'] \
        = current_restaurant_df['category tags'] \
        .apply(lambda x: calculate_score(taste_votes, tags_list=x))

    # select the top_n or all, sorted restaurants
    df = current_restaurant_df.sort_values(by='votes', ascending=False)
    print(df.shape)
    top_n = max(min(len(df)-8, 50), 5)
    print('top_n = '+str(top_n))
    output = df.head(top_n)
    print(output[['business_id','10 tags for food categories']])
    return output
