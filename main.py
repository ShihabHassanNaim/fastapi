from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS (Frontend Access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
app.mount("/", StaticFiles(directory="public", html=True), name="static")

# DB Connection
def db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "movie_info"),
        cursorclass=pymysql.cursors.DictCursor
    )

# Pydantic Model
class MovieInput(BaseModel):
    Movie_Name: str
    Genre: str
    Year: int
    IMDb_Rating: float
    Director_ID: int

# Fetch All Movies
@app.get("/movie")
def get_movies():
    conn = db()
    cur = conn.cursor()

    sql = """
    SELECT m.Movie_ID, m.Movie_Name, m.Genre, m.Year, m.IMDb_Rating,
           d.Director_Name
    FROM Movie m
    LEFT JOIN Director d ON m.Director_ID = d.Person_ID
    ORDER BY m.Movie_ID DESC
    """
    cur.execute(sql)
    movies = cur.fetchall()

    cur.close()
    conn.close()
    return movies

# Add Movie
@app.post("/movie")
def add_movie(movie: MovieInput):
    conn = db()
    cur = conn.cursor()

    sql = """
    INSERT INTO Movie (Movie_Name, Genre, Year, IMDb_Rating, Director_ID)
    VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(sql, (movie.Movie_Name, movie.Genre, movie.Year,
                      movie.IMDb_Rating, movie.Director_ID))
    conn.commit()

    cur.close()
    conn.close()
    return {"message": "Movie added"}

# Delete Movie
@app.delete("/movie/{id}")
def delete_movie(id: int):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Movie WHERE Movie_ID=%s", (id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Movie not found")

    cur.execute("DELETE FROM Movie WHERE Movie_ID=%s", (id,))
    conn.commit()

    cur.close()
    conn.close()
    return {"message": "Movie deleted", "id": id}
