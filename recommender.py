import pandas as pd
import json

def load_data():
    df = pd.read_csv('movies_metadata.csv', low_memory=False)
    df = df[df['release_date'].notna()]
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    df['genre_list'] = df['genres'].apply(parse_genres)
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
    return df

def parse_genres(genres_str):
    try:
        genres_data = json.loads(genres_str.replace("'", '"'))
        return [genre['name'] for genre in genres_data]
    except Exception:
        return [] 

def recommend_movies(df, genre=None, year=None):
    recommendations = df.copy()

    if year:
        recommendations = recommendations[recommendations['release_year'] == year]

    if genre:
        recommendations = recommendations[recommendations['genre_list'].apply(lambda genres: genre in genres)]

    recommendations = recommendations.sort_values(by=['vote_average', 'popularity'], ascending=False)

    if recommendations.empty:
        return []

    return recommendations.head(5).to_dict(orient='records')
