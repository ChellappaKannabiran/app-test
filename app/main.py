# main.py

# Based on blog post https://kinsta.com/blog/fastapi/
# Further reading: https://fastapi.tiangolo.com/tutorial/first-steps/
# https://codingnomads.co/blog/python-fastapi-tutorial

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from schema import Genre, Stock, Album, UpdateAlbum
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer


# Create FastAPI instance
app = FastAPI(
	title='Vinyl Records Database API',
	description='An API for a simple python app. In this example, an SQL database is constructed \
                     to store information relating to the stock held by an imaginary vinyl record shop. \
                     The API allows users to view, add and delete entries in the database, \
                     and update existing entries to say whether the albums listed are curently in stock or not.' )

#SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///./db/test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create DB class; instances of this class will be used to fetch and insert rows into the database
class DBAlbum(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String(50))
    album_name = Column(String(50))
    condition = Column(String(50))
    notes = Column(String, nullable=True)
    genre = Column(String(50))
    stock = Column(String(50))

Base.metadata.create_all(bind=engine)

# Define CRUD API endpoints using FastAPI
# ---------------------------------------

# Define endpoint to submit a new album entry via the @app.post decorator
@app.post('/api/v1/albums')
# Create new function 'create_album' which accepts an instance of the Album class, and returns it
def create_album(album: Album, db: Session = Depends(get_db)):
    db_album = DBAlbum(**album.dict())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

# Define endpoint to return the contents of the database via the @app.get decorator
@app.get('/api/v1/albums/')
def view_all_albums(db: Session = Depends(get_db)):
    return db.query(DBAlbum).all()

# Define endpoint to return the contents of the database for a specific artist
@app.get('/api/v1/albums/{artist_name}')
def view_albums_by_artist(artist_name: str, db: Session = Depends(get_db)):
    artist = db.query(DBAlbum).filter(DBAlbum.artist_name == artist_name).all()
    if not artist:
       raise HTTPException(status_code=404, detail=f"Query database failed, artist {artist_name} not found.")
    else:
       return artist

# Define endpoint to return all albums by condition (either new or pre-loved)
@app.get('/api/v1/condition/{condition}')
def view_albums_by_condition(condition: str, db: Session = Depends(get_db)):
    filter_condition = db.query(DBAlbum).filter(DBAlbum.condition == condition).all()
    if not filter_condition:
       raise HTTPException(status_code=404, detail=f"Query database failed, condition {condition} not found.")
    else:
       return filter_condition

# Define endpoint to return all albums by stock (either in or out)
@app.get('/api/v1/stock/{stock}')
def view_albums_by_stock(stock: str, db: Session = Depends(get_db)):
    filter_stock = db.query(DBAlbum).filter(DBAlbum.stock == stock).all()
    if not filter_stock:
       raise HTTPException(status_code=404, detail=f"Query database failed, stock {stock} not found.")
    else:
       return filter_stock

# Define endpoint to delete album entry from database via the @app.delete decorator
@app.delete("/api/v1/albums/{album_id}")
# Create the 'delete_album' function, which takes in the existing album's unique ID
def delete_album(album_id: int, db: Session = Depends(get_db)):
   db_album = db.query(DBAlbum).filter(DBAlbum.id == album_id).first()
   if not db_album:
      raise HTTPException(status_code=404, detail=f"Delete album failed, id {album_id} not found.")
   else:
      db.query(DBAlbum).filter(DBAlbum.id == album_id).delete()
      db.commit()
      raise HTTPException(status_code=200, detail=f"Album found, id {album_id} deleted.")  

# Define endpoint to update an album's details, in this case, whether in or out of stock, via the @app.put decorator
@app.put("/api/v1/albums/{id}")
# Create method 'update_album_stock', which takes an instance of the UpdateAlbum class and the album id:
def update_album_stock(album_update: UpdateAlbum, album_id: int, db: Session = Depends(get_db)):
    db_album = db.query(DBAlbum).filter(DBAlbum.id == album_id).first()
    if not db_album:
       raise HTTPException(status_code=404, detail=f"Could not find album with id: {id}")
    else:
       if album_update.stock is not None:
          print(db_album)
          db_album.stock = album_update.stock
          db.commit()
          db.refresh(db_album)
          return db_album
       else:
          raise HTTPException(status_code=404, detail=f"Value of stock not valid {id}")

@app.get("/")
async def root():
 return {"greeting":"Hello world"}
