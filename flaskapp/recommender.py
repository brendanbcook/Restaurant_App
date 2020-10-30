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

# Make a single user test input for the model from list Review objects
def make_input(reviews):
    restaurant_names = [review.name for review in reviews]
    user_ratings = [review.rating for review in reviews]
    train, item_features, names= load_training_data()
    rating_vector = np.zeros(names.shape[0])
    sorted_index = np.searchsorted(names, restaurant_names)
    for i, res_name in enumerate(restaurant_names):
        if names[sorted_index[i]].lower() == res_name.lower():
            if rating_vector[sorted_index[i]] == 0:
                rating_vector[sorted_index[i]] = user_ratings[i]
            else:
                rating_vector[sorted_index[i]] += user_ratings[i]
                rating_vector[sorted_index[i]] /= 2.0
    return rating_vector
# Run the recommendation model, return a list of the names of the top k recommended restaurants
def predict(rating_vector, item_indices=None, k=100):
    model = load_model()
    train, item_features, names = load_training_data()
    if item_indices:
        assert item_indices.shape[0] == names.shape[0]
        prediction = model.predict(rating_vector, item_indices)
    else:
        prediction = model.predict(rating_vector, np.arange(names.shape[0]))
    sorted_indices = np.argsort(prediction)
    sorted_recommendations = names[sorted_indices]
    return sorted_recommendations[:k]
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

