import pickle
import pandas as pd

from sklearn.neighbors import KDTree

class BookRecommender():

    def k_neighbors(self, data, target, k=3):
        if(len(data) < 3):
            k = len(data)

        bow_vector = pickle.load(open('./apps/recommender/pickle/bow_vector.pickle', 'rb'))

        data_bow = bow_vector.transform(data).toarray()
        target_bow = bow_vector.transform(pd.Series(target)).toarray()

        tree = KDTree(data_bow, leaf_size=2)
        _, idx = tree.query(target_bow, k=k)

        return idx[0]