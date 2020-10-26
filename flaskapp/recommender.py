import pandas as pd
import numpy as np
import scipy
import pickle
import os
from lightfm import LightFM
from lightfm.evaluation import precision_at_k

from flaskapp.preprocess import load_training_data

def train_model():
    train, item_features, names = load_training_data()
    model = LightFM(loss='warp', no_components=50)
    model.fit(train, epochs=100)
    save_model(model)

# Make a single user test input for the model from list of restaurant names and ratings
def make_input(restaurant_names, user_ratings):
    train, item_features, names= load_training_data()
    rating_vector = np.zeros(names.shape[0])
    sorted_index = np.searchsorted(names, restaurant_names)
    for i, res_name in enumerate(restaurant_names):
        if names[sorted_index[i]].lower() == res_name.lower():
            rating_vector[sorted_index[i]] = user_ratings[i]
def predict(rating_vector, item_indices=None):
    model = load_model()
    train, item_features, names = load_training_data()
    if item_indices:
        assert item_indices.shape[0] == names.shape[0]
        return model.predict(rating_vector, item_indices)
    else:
        return model.predict(rating_vector, np.arange(names.shape[0]))
def save_model(model):
    filename = 'data/recommender'
    pickle.dump(model, open(filename, 'wb'))
def load_model():
    filename = 'data/recommender'
    if not os.path.exists(filename):
        raise Exception('There is no saved model at '+filename)
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

