import pandas as pd
import numpy as np


def normalize_column (col, max_val):
    col_max = col.max()
    col_min = col.min()
    col = (col - col_min)/(col_max-col_min)*max_val
    return col


def calc_distance(a, b):
    b = b.iloc[0,:]
    distance = np.sqrt(sum((a - b) ** 2))
    return distance


def find_movie_title(data_set, title):
    title = title.title()
    data_set = data_set.loc[data_set['title'].str.find(title) != -1 ]
    movie_options = list(data_set.iloc[:, 0])
    if not movie_options:
        print("Oops! We don't have such a movie!")
        return 0
    elif len(movie_options) == 1:
        return movie_options[0]
    elif len(movie_options)>1:
        print("Looks like we have multiple options! \nChoose:")
        for option in movie_options:
            print('\t{i} for \'{option}\''.format(option=option, i=movie_options.index(option)+1))
        user_choice = -1
        print('Pick a number: ')
        while (user_choice < 1 or user_choice > len(movie_options)) :
            user_choice = int(input())
        chosen_title = movie_options[user_choice - 1]
        return chosen_title


def create_query(data_set, kwargs):
    col_list = list(data_set.columns)
    
    # creating query filled with zeros
    basic_query = data_set.loc[data_set['title'] == 'M (1931)' ] * 0

    # filling non-class features (without title) with maximum available values
    for col in col_list[1:9]:
        max_val =  data_set.loc[:,col].max()
        basic_query.loc[:,col] = max_val
        
    # adjusting class values given kwargs 
    for key in kwargs:
        if (key in col_list):
            basic_query.loc[:,key] = kwargs[key]

    return basic_query


def make_recommendation(title, recommended):
    if title=='':
        rec_based_on = 'for given preferences'
    else:
        rec_based_on = 'based on the movie {movie}'.format(movie=title)
    print("\nRecommendations ({based}):".format(based=rec_based_on))
    for movie in recommended.values:
        print('\t - {movie}'.format(movie=movie))
    print('')


def find_n_recommendations(data_set, n, chosen_title = '', **kwargs):
    movie_title = chosen_title
    if chosen_title == '':                # case when movie title not provided
        query = create_query(data_set, kwargs)
    else:                                 # case when movie title is provided
        chosen_title = find_movie_title(data_set, chosen_title)
        query = data_set[data_set['title']==chosen_title]
        if query.empty:
            return 0
        else:
            movie_title = query.iloc[0,0]
            
    column_names = data_set.columns.values   # column names for iterations
    query = query.iloc[:,1:]                 # removing title from query
    data_set = data_set[data_set['title']!=chosen_title] 

    distances = []
    print('\nSearching for best movies...')
    for index, row in data_set.iterrows():
        distances.append(calc_distance(row[column_names[1:]], query))
        
    data_set.loc[:, 'distance'] = distances
    recommendations = data_set.nsmallest(n, 'distance')
    recommended_titles = recommendations.loc[:,'title']
    
    make_recommendation(movie_title, recommended_titles)
    
    return recommended_titles


# reading data
df = pd.read_csv('imdb.csv', error_bad_lines = False, warn_bad_lines=False)

# handling empty values
df = df.dropna()

# deleting unnecessary features
df = df.drop(columns=['fn', 'tid', 'wordsInTitle', 'url', 'type', 
                 'nrOfPhotos', 'nrOfGenre'])


# normalizing non-class features
to_normalize = [('ratingCount', 1), ('imdbRating', 1), ('duration', 0.25), ('year', 0.25), ('nrOfWins', 1),
                ('nrOfNominations', 0.25), ('nrOfNewsArticles', 0.5), ('nrOfUserReviews', 1)]


for col in to_normalize:
    df[col[0]] = normalize_column(df[col[0]],col[1])

find_n_recommendations(df, 3, Action = 1, Adult = 0, SciFi = 1)
find_n_recommendations(df, 5, 'Toy Story')
find_n_recommendations(df, 5, 'Batman Begins')
find_n_recommendations(df, 5, 'Star Wars: Episode III')
