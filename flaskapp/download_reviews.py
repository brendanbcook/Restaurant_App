import pandas as pd
import numpy as np
import requests

def get_api_key(filename):
    with open(filename) as f:
        return f.readline()
api_key = get_api_key('api_key.txt')
def make_business_df(business_data):
    businesses = business_data['businesses']
    ids = [elt['id'] for elt in businesses]
    business_name = [elt['name'] for elt in businesses]
    address = [elt['location']['address1'] for elt in businesses]
    zip_codes = [elt['location']['zip_code'] for elt in businesses]
    phones = [elt['display_phone'] for elt in businesses]
    urls = [elt['url'] for elt in businesses]
    ratings = [elt['rating'] for elt in businesses]
    df = pd.DataFrame(data={'name': business_name, 'rating': ratings, 'address': address, 'zip_code': zip_codes, 'phone': phones, 'url': urls, 'id': ids})
    return df
def make_review_df(review_data):
    data = [(elt['rating'], elt['text'], elt['time_created'], elt['id'], elt['user']['name'], elt['user']['id']) for elt in review_response['reviews']]
    review_df = pd.DataFrame(data=data, columns=['rating', 'review', 'timestamp', 'restaurant_id', 'user_name', 'user_id'])
    return review_df
def combine_data(df, filename):
    try:
        big_df = pd.read_csv(filename, index_col=0)
    except:
        raise ValueError('invalid filename')
    bigger_df = pd.concat([big_df, df])
    bigger_df.reset_index()
    bigger_df.to_csv(filename, index=False)
def query_business_api(offset=1):
    business_endpoint = 'https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': f'bearer {api_key}'}
    PARAMETERS = {'location': 'Minneapolis, MN', 'limit':50, 'offset': offset}
    business_response = requests.get(url=business_endpoint, params=PARAMETERS, headers=HEADERS)
    return business_response.json()
def query_review_api(key):
    review_endpoint = f'https://api.yelp.com/v3/businesses/{id_key}/reviews'
    return requests.get(url=review_endpoint, headers=HEADERS).json()

def process_review_batch():
    business_data = query_business_api()
    business_df = make_business_df(business_data)
    combine_data(business_df, 'business_data.csv')

    review_df = pd.DataFrame(columns=['rating', 'review', 'timestamp', 'restaurant_id', 'user_name', 'user_id'])
    for id_key in df['id'].values:
        review_response = query_review_api(id_key)
        new_reviews = make_review_df(review_response)
        review_df = pd.concat([review_df, new_reviews])
    combine_data(review_df, 'review_data.csv')
def update_training_data():
    review_df = pd.read_csv('review_data.csv')
    review_df = reviews.loc[:, ['user_id', 'restaurant_id', 'rating']]
    review_df.to_csv('train.csv', index=False)