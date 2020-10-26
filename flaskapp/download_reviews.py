import pandas as pd
import numpy as np
import requests
import os

def get_api_key(filename):
    with open(filename) as f:
        return f.readline()
def make_business_df(business_data, offset):
    businesses = business_data['businesses']
    data = []
    for elt in businesses:
        if 'price' in elt.keys():
            data_entry = (elt['name'], elt['rating'], elt['location']['address1'], elt['location']['zip_code'], elt['display_phone'], elt['url'], elt['id'], elt['price'], elt['transactions'], elt['categories'], elt['coordinates'], offset)
        else:
            data_entry = (elt['name'], elt['rating'], elt['location']['address1'], elt['location']['zip_code'], elt['display_phone'], elt['url'], elt['id'], '', elt['transactions'], elt['categories'], elt['coordinates'], offset)
        data.append(data_entry)
    df = pd.DataFrame(data=data, columns=['name', 'rating', 'address', 'zip_code', 'phone', 'url', 'restaurant_id', 'price', 'transactions', 'categories', 'coordinates', 'query_offset'])
    return df
def make_review_df(review_list, restaurant_id, restaurant_name):
    data = [(elt['rating'], elt['text'], elt['time_created'], elt['id'], elt['user']['name'], elt['user']['id'], restaurant_id, restaurant_name) for elt in review_list]
    review_df = pd.DataFrame(data=data, columns=['rating', 'review', 'timestamp', 'review_id', 'user_name', 'user_id', 'restaurant_id', 'restaurant_name'])
    return review_df
def save_data(df, filename):
    if os.path.exists(filename):
        big_df = pd.read_csv(filename, index_col=0)
        bigger_df = pd.concat([big_df, df])
    else:
        bigger_df = df
    bigger_df.reset_index()
    bigger_df.to_csv(filename, index=False)
def query_business_api(offset, api_key):
    business_endpoint = 'https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': f'bearer {api_key}'}
    PARAMETERS = {'location': 'Minneapolis, MN', 'limit': 50, 'offset': offset, 'term': 'restaurants'}
    business_response = requests.get(url=business_endpoint, params=PARAMETERS, headers=HEADERS)
    return business_response.json()
def query_review_api(id_key, api_key):
    HEADERS = {'Authorization': f'bearer {api_key}'}
    review_endpoint = f'https://api.yelp.com/v3/businesses/{id_key}/reviews'
    return requests.get(url=review_endpoint, headers=HEADERS).json()
def process_business_batch(offset, api_key):
    review_path = 'data/review_data.csv'
    business_path = 'data/business_data.csv'
    business_data = query_business_api(offset, api_key)
    business_df = make_business_df(business_data, offset)
    save_data(business_df, business_path)
    # review_df = pd.DataFrame(columns=['rating', 'review', 'timestamp', 'restaurant_id', 'user_name', 'user_id'])
    # for id_key in business_df['restaurant_id'].values:
    #     review_response = query_review_api(id_key, api_key)
    #     new_reviews = make_review_df(review_response['reviews'])
    #     review_df = pd.concat([review_df, new_reviews])
    # save_data(review_df, review_path)
