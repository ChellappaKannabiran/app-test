# schema.py
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class Genre(str, Enum):
   rock = "Classic rock"
   jazz = "Jazz fusion"
   pop = "Pop"
   avantgarde = "Avant garde"

class Stock(str, Enum):
   instock = "In stock"
   outstock = "Out of stock"

class Condition(str, Enum):
   new = "New"
   preloved = "Pre-loved"

class Album(BaseModel):
   # Define attributes of the Album class
   artist_name: str
   album_name: str
   condition: Condition
   notes: Optional[str] = None
   genre: Genre
   stock: Stock
 
   class Config:
     orm_mode = True

class UpdateAlbum(BaseModel):
   stock: Optional[Stock]
