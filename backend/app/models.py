from pydantic import BaseModel
from typing import List

class MusicList(BaseModel):
    urls: List[str]
    format: str = "mp3"  

class Music(BaseModel):
    url: str
    format: str = "mp3"
