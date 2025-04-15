from pydantic import BaseModel
from typing import List, Optional

class MovieResponse(BaseModel):
    title: Optional[str]
    release_year: Optional[int]
    genre_list: List[str]
    vote_average: Optional[float]
    overview: Optional[str]
