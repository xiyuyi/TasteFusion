import pickle
import os

def get_initial_restaurants(center:list = None,
                            search_radius:float = None,
                            mock=False,
                            datapath = None):
    """
    This function will return the initial pool of restaurants as a dataframe
    :param center:
    :param range:
    :param mock:
    :return:
    """
    restaurants_df = []
    if mock:
        file_path = os.path.join(datapath, 'df_restaurants_Reno_shortlist_wtags_n_categorytags.pkl')
        with open(file_path, 'rb') as f:
            restaurants_df = pickle.load(f)
    return restaurants_df
