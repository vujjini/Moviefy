import requests
import json
from flask import render_template


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", message = message)

def trailer(movie_id):
    url = f"http://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=39efdc94b5e403f01fd0d0343658a990"
    response = requests.get(url)
    if response.status_code == 200:
        array = response.json()
        text = json.dumps(array)
        dataset = json.loads(text)
        for i in dataset["results"]:
            if i["type"] == 'Trailer':
                trailer_key = i["key"]
                trailer_link = f"https://www.youtube.com/watch?v={trailer_key}"
                return(trailer_key)
    else:
        return ("error")
