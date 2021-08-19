import os
import random
import re
from tmdbv3api import TMDb
from tmdbv3api import Movie

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from datetime import datetime
from helpers import apology

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


tmdb = TMDb()
tmdb.api_key = '39efdc94b5e403f01fd0d0343658a990'
movie = Movie()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inputs", methods = ["GET", "POST"])
def inputs():
    if request.method == 'GET':
        return render_template("input.html")
    if request.method == 'POST':
        # list of recommended movies
        movies = []
        title1 = request.form.get("title_1").upper()
        title2 = request.form.get("title_2").upper()

        if not title1 and not title2:
            return apology("Come on! You've gotta have a favourite movie")

        if title1:
            x = movie.search(title1) # getting a list of movies with that name
            title1 = re.sub(r'[^\w\s]', '', title1)
            if len(x) < 1:
                return apology("What you've inputted is either a TV show or a movie released in a parallel universe")
            title1_id = 0
            for item in x:
                original_title1 = item["original_title"].upper()
                if title1 in re.sub(r'[^\w\s]', '', original_title1) or re.sub(r'[^\w\s]', '', original_title1) in title1:
                    title1_id = item["id"]
                    break
                else:
                    title1_id = None
            print(original_title1, title1_id)
            # ensuring that title1 exists
            if title1_id == None or title1_id == 0:
                title1 = None
            else:
                recommendations1 = movie.recommendations(movie_id=title1_id)
                for item in recommendations1:
                    movies.append(item["original_title"])

        if title2:
            title2 = re.sub(r'[^\w\s]', '', title2)
            y = movie.search(title2)  # getting a list of movies with that name
            title2_id = 0
            for item in y:
                original_title2 = item["original_title"].upper()
                if title2 in re.sub(r'[^\w\s]', '', original_title2) or re.sub(r'[^\w\s]', '', original_title2) in title2:
                    title2_id = item["id"]
                    break
                else:
                    title2_id = None
            print(original_title2)
            if title2_id == None or title2_id == 0:
                title2 = None
            else:
                recommendations2 = movie.recommendations(movie_id=title2_id)
                for item in recommendations2:
                    movies.append(item["original_title"])

        if len(movies) > 0:
            if title1 in movies:
                movies.remove(title1)
            if title2 in movies:
                movies.remove(title2)
            random_movie = random.choice(movies) # returns a random movie from the recommended movies list
            z = movie.search(random_movie)
            for item in z:
                if item["original_title"] == random_movie:
                    random_movie_poster = item.poster_path
                    break
            print(random_movie_poster)
            print(movies)
            return render_template("generate.html", movie = random_movie, poster = random_movie_poster)
        else:
            return apology("I'm sorry but I did'nt watch this movie, so i coud'nt find any recommendations.")
