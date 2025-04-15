from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os

app = FastAPI()

# Allow frontend domain only (or "*" during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Data Once on Startup
@app.on_event("startup")
def load_data():
    global df
    df = pd.read_csv('movies_metadata.csv', low_memory=False)
    df = df[df['release_date'].notna()]
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    df['genre_list'] = df['genres'].apply(parse_genres)
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')

def parse_genres(genres_str):
    try:
        genres_data = json.loads(genres_str.replace("'", '"'))
        return [genre['name'] for genre in genres_data]
    except:
        return []

@app.get("/")
def root():
    return {"message": "Backend Running!"}

@app.get("/genres")
def get_genres():
    genres = df['genre_list'].explode().dropna().unique().tolist()
    genres.sort()
    return genres

@app.get("/recommend")
def recommend_movies(genre: str = None, year: int = None):
    filtered = df.copy()
    if year:
        filtered = filtered[filtered['release_year'] == year]
    if genre:
        filtered = filtered[filtered['genre_list'].apply(lambda x: genre in x)]
    results = filtered.sort_values(by=['vote_average', 'popularity'], ascending=False)
    return results.head(5).to_dict(orient='records')

@app.get("/search")
def search_movies(query: str):
    filtered = df[df['title'].str.contains(query, case=False, na=False)]
    results = filtered.sort_values(by=['vote_average', 'popularity'], ascending=False)
    return results.head(10).to_dict(orient='records')

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
