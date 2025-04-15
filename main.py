from fastapi import FastAPI, Query
from typing import Optional, List
from recommender import load_data, recommend_movies
from models import MovieResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

df = load_data()

@app.get("/")
def root():
    return {"message": "Movie Recommender API"}

@app.get("/recommend", response_model=List[MovieResponse])
def get_recommendations(
    genre: Optional[str] = Query(None),
    year: Optional[int] = Query(None)
):
    return recommend_movies(df, genre, year)

@app.get("/genres", response_model=List[str])
def get_genres():
    genres = df['genre_list'].explode().dropna().unique().tolist()
    genres.sort()
    return genres


@app.get("/search", response_model=List[dict])
def search_movies(query: str = Query(..., min_length=1)):
    results = df[df['title'].str.contains(query, case=False, na=False)]
    results = results.sort_values(by=['vote_average', 'popularity'], ascending=False)
    return results.head(10).to_dict(orient='records')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)