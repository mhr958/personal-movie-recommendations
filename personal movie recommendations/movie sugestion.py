import requests
import json


def get_movies_from_tastedive(name):
    base_url = 'https://tastedive.com/api/similar'
    query_param = {'q': name, 'type': 'movies', 'limit': 5, 'k': my_key2}
    resp = requests.get(base_url, params=query_param)
    py_data_dict = resp.json()
    return py_data_dict


def extract_movie_titles(py_data_dict):
    suggestion = [elem['Name'] for elem in py_data_dict['Similar']['Results']]
    return suggestion


def get_related_titles(movie_list):
    recommended_movie_list = []
    for movie in movie_list:
        recommendation_dict = get_movies_from_tastedive(movie)
        recommendation_list = extract_movie_titles(recommendation_dict)
        for title in recommendation_list:
            if title not in recommended_movie_list:
                recommended_movie_list.append(title)
    return recommended_movie_list


def get_movie_data(name):
    base_url = 'http://www.omdbapi.com/'
    query_param = {'t': name, 'r': 'json', 'apikey': my_key}
    resp = requests.get(base_url, params=query_param)
    py_data_dict = resp.json()
    return py_data_dict


def get_movie_rating(py_data_dict):
    RT_rating_list = [elem['Value'] for elem in py_data_dict['Ratings']
                      if elem['Source'] == 'Rotten Tomatoes']
    if len(RT_rating_list) == 0:
        rating = 0
    else:
        rating = int(RT_rating_list[0].replace('%', ''))
    return rating


def sort_pair(title_rating_pair_list):
    return sorted(title_rating_pair_list, key=lambda pair: (pair[1], pair[0]), reverse=True)


def get_sorted_recommendations(titles_list):
    recommendations_title_rating_pair = []
    related_titles = get_related_titles(titles_list)
    for title in related_titles:
        title_data_dict = get_movie_data(title)
        title_rating = get_movie_rating(title_data_dict)
        recommendations_title_rating_pair.append((title, title_rating))
    return [pair[0] for pair in sort_pair(recommendations_title_rating_pair)]


titles = input("Enter some movie titles to get recommendations: ")
my_key = input("Enter OMDb api key: ")
my_key2 = input("Enter tastedive api key: ")
titles_list = titles.split(', ')
print(get_sorted_recommendations(titles_list))
