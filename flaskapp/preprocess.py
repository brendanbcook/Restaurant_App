import pandas as pd
import numpy as np
import scipy
from flaskapp import db

def update_training_data():
    # Convert review_df to training matrix
    review_df = pd.read_csv('data/full_review_data.csv')
    review_df.drop_duplicates(subset = ['user_id', 'restaurant_id'], keep='first', inplace=True)
    review_df = review_df[~review_df['restaurant_name'].isnull()]
    bus_df = pd.read_csv('data/business_data.csv')
    bus_df = bus_df[bus_df['name'].isin(review_df['restaurant_name'])]
    bus_df.drop_duplicates(subset='name', keep='first', inplace=True)
    bus_df.sort_values(by='name', inplace=True)
    review_df = review_df[['user_id', 'restaurant_name', 'rating']]
    name_series = bus_df['name']
    pivoted = pd.pivot(review_df, index='user_id', columns='restaurant_name', values='rating')
    pivoted.fillna(value=0, inplace=True)
    item_df = process_item_features(bus_df)
    np.savez_compressed('data/train.npz',  train=pivoted, item_features=item_df, names=name_series.values)
def process_item_features(bus_df):
    # Preprocessing the restaurant-level features
    item_features = bus_df.loc[:, ['price', 'rating', 'transactions']]
    item_features.index = bus_df['name']
    item_features = item_features[~item_features.index.isnull()]
    item_features['has_pickup'] = item_features['transactions'].apply(lambda li: 'pickup' in li)
    item_features['has_delivery'] = item_features['transactions'].apply(lambda li: 'delivery' in li)
    bool_dict = {False: 0, True: 1}
    item_features['has_pickup'] = item_features['has_pickup'].map(lambda x: bool_dict[x])
    item_features['has_delivery'] = item_features['has_delivery'].map(lambda x: bool_dict[x])
    item_features.drop('transactions', axis=1, inplace=True)
    def price_mapping(s):
        d = {np.nan: 0, '$':1, '$$': 2, '$$$': 3, '$$$$': 4}
        return d[s]
    item_features['price'] = item_features['price'].map(price_mapping)
    return item_features

def load_training_data():
    A = np.load('data/train.npz', allow_pickle=True)
    train = scipy.sparse.coo_matrix(A['train'])
    item_features = scipy.sparse.coo_matrix(A['item_features'])
    names = A['names']
    return train, item_features, names


# Populate Business table in database
def create_business_table():
    names = pd.read_csv('data/names.csv')
    for i in range(len(names)):
        name, category, coord = names.iloc[i, :]
        business = Business(name=name, coordinates=coord, categories=category)
        db.session.add(business)
    db.session.commit()