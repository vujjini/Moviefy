import os
import random
import re
from tmdbv3api import TMDb
from tmdbv3api import Movie

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from helpers import apology, trailer
from difflib import SequenceMatcher

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


tmdb = TMDb()
tmdb.api_key = '39efdc94b5e403f01fd0d0343658a990'
movie = Movie()
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


@app.route("/")
def index():
    session["data"] = []
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
            title1 = re.sub('[\W_]+', '', title1)
            if len(x) < 1:
                return apology("What you've inputted is either a TV show or a movie released in a parallel universe")
            title1_id = 0
            similarity_dict = {}
            for item in x:
                original_title1 = item["original_title"].upper()
                similarity_score = similar(re.sub('[\W_]+', '', original_title1), title1.upper())
                similarity_dict[item] = similarity_score
                # if title1 in re.sub(r'[^\w\s]', '', original_title1) or re.sub(r'[^\w\s]', '', original_title1) in title1:
                # print(re.sub('[\W_]+', '', original_title1), title1.upper())
                # if title1.upper() == re.sub('[\W_]+', '', original_title1): #there is something WRONG WITH THIS LINE: FIX IT!!!!!!!!!!!!!!!!!! || ***UPDATE: found the problem. we aren't accounting for the fact that what if certain special characters like & can be input as "and" but the program doesn't know that.
                #     print("YESSIRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                #     title1_id = item["id"]
                #     break
                # elif title1.upper() in re.sub('[\W_]+', '', original_title1) or re.sub('[\W_]+', '', original_title1) in title1.upper(): #there is something WRONG WITH THIS LINE: FIX IT!!!!!!!!!!!!!!!!!!
                #     print("YESSIRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                #     title1_id = item["id"]
                #     break
                # else:
                #     title1_id = None
            item = max(similarity_dict, key=similarity_dict.get) #using similarity score to obtain the right title a user looks for
            title1_id = item["id"]
            print("hi")
            print(item["id"])
            print("bye")
            print(item["original_title"])
            print(len(movie.recommendations(movie_id=title1_id))) #for some reason the API can't find recommendations for 'The good, the bad and the ugly'
            # print(original_title1, title1_id)
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
            for i in session["data"]:
                if i in movies:
                    movies.remove(i)
            if len(movies) == 0:
                movies = session["data"]
                session["data"] = []

            random_movie = random.choice(movies) # returns a random movie from the recommended movies list
            z = movie.search(random_movie)
            for item in z:
                # if item["original_title"] in session["data"]:
                #     print(item["original_title"])
                #     movies.remove(item["original_title"])
                # else:
                #     session["data"].append(item["original_title"])
                if item["original_title"] == random_movie:
                    session["data"].append(item["original_title"])
                    random_movie_poster = item.poster_path
                    trailer_key = trailer(item["id"])
                    break
            # print(random_movie_poster)
            # print(trailer_key)
            print(session["data"])
            print(movies)
            # print(movies)
            return render_template("generate.html", movie = random_movie, poster = random_movie_poster, key = trailer_key)
        else:
            return apology("I'm sorry but I did'nt watch this movie, so i couldn't find any recommendations.")
