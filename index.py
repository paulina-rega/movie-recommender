import pandas as pd
import numpy as np



def normalize_column (col):
    col_max = col.max()
    col_min = col.min()
    col = (col - col_min)/(col_max-col_min)
    return col


def calc_distance(a ,b):
    b = b.iloc[0,:]
    distance = np.sqrt(sum((a-b)**2))
    return distance


def create_query(data_set, **kwargs):
    return 0


def find_n_recommendations(chosen_title, data_set, n):
    #TODO capitalize df 'title'
    query = data_set[data_set['title']==chosen_title]
    
    if query.empty:
        print("ups :( nie mamy tego filmu w bazie")
        return 0
    
    column_names = data_set.columns.values
    query = query.iloc[:,1:]
    data_set = data_set[data_set['title']!=chosen_title]

    distances = []
    for index, row in data_set.iterrows():
        distances.append(calc_distance(row[column_names[1:]], query))
        
    data_set.loc[:, 'distance'] = distances
    
    data_set = data_set.sort_values(by=['distance'])
    return data_set


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

titles_and_dist = find_n_recommendations('Pocahontas (1995)', df, 3)

#titles_and_dist = find_n_recommendations('Ice Age 2 - Jetzt taut\'s (2006)', df, 3)

