import pandas as pd
import numpy as np


def normalize_column (col):
    col_max = col.max()
    col_min = col.min()
    col = (col - col_min)/(col_max-col_min)
    return col


def calc_distance(a ,b):
    distance = np.sqrt(sum((a-b)**2))
    return distance

def create_query(data_set, **kwargs):
    return 0

def find_n_recommendations(chosen_title, data_set, n):
    #zrobic capitalize title na df
    query = data_set[data_set['title']==chosen_title]
    
    if query.empty:
        print("ups :( nie mamy tego filmu w bazie")
        return 0
    data_set = data_set[data_set['title']!=chosen_title]
    
    titles_and_distances = pd.DataFrame(columns=['title', 'distance'])
    
    no_of_rows = data_set.shape[0]

    for i in range(no_of_rows):
        distance = calc_distance(query.iloc[0][1:], data_set.iloc[i][1:])
        title = data_set.iloc[i]['title'] 
        distance_entry = pd.DataFrame([[title, distance]], 
                                      columns=['title', 'distance'])
        titles_and_distances = titles_and_distances.append(distance_entry)
        
    ## TODO : wybierz kilka najbliższych :) sortowanie nie działa 
    titles_and_distances = titles_and_distances.sort_values(by=['distance'])
    return titles_and_distances

    
    





# reading data
df = pd.read_csv('imdb.csv', error_bad_lines = False, warn_bad_lines=False)

# handling empty values and deleting unnecessary features
df = df.dropna()
df = df.drop(columns=['fn', 'tid', 'wordsInTitle', 'url', 'type', 
                 'nrOfPhotos', 'nrOfGenre'])


# normalizing non-class features
to_normalize = ['ratingCount', 'imdbRating', 'duration', 'year', 'nrOfWins',
                'nrOfNominations', 'nrOfNewsArticles', 'nrOfUserReviews']
for col_name in to_normalize:
    df[col_name] = normalize_column(df[col_name])
    

    
dist = calc_distance(df.iloc[0][1:], df.iloc[1][1:])
dist2 = calc_distance(df.iloc[0][1:], df.iloc[0][1:])

#titles_and_dist = find_n_recommendations('Pocahontas (1995)', df, 3)


titles_and_dist = find_n_recommendations('Ice Age 2 - Jetzt taut\'s (2006)', df, 3)

