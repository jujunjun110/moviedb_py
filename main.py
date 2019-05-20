import os
import json
import urllib
import tmdbsimple as tmdb


def fetch_infomations():
    json_filepath = "results/result.json"
    key = os.environ.get("API_KEY")

    if key is None:
        raise Exception("Please set your API KEY in .env file ")

    tmdb.API_KEY = key
    target_movie_ids = [
        447404,  # Detective Pikachu
        299534,  # Avengers Endgame
        109445,  # Frozen
        335984,  # Blade Runner 2049 (because we already have a poster, it is easy to show demo for visitor)
        315011,  # Shin Godzilla
        118,  # Charlie and the Chocolate Factory
    ]

    movies = [fetch_movie_detail(movie_id) for movie_id in target_movie_ids]

    with open(json_filepath, "w") as f:
        json.dump(movies, f, indent=4)


def download_images():
    target_filepath = "results/result.json"
    tmdb.API_KEY = os.environ.get("API_KEY")

    with open(target_filepath, "r") as f:
        movies = json.loads(f.read())

    poster_images = flatten([m["posters"] for m in movies])

    for path in poster_images:
        url = "https://image.tmdb.org/t/p/w1280" + path
        print(url)
        data = urllib.request.urlopen(url).read()
        dst_path = "results/images/posters/" + path
        with open(dst_path, mode="wb") as f:
            f.write(data)

    director_images = [m["director"]["profile_path"] for m in movies]
    cast_images = [c["profile_path"] for c in flatten([m["casts"] for m in movies])]
    people_images = director_images + cast_images

    for path in people_images:
        url = "https://image.tmdb.org/t/p/w1280" + path
        print(url)
        data = urllib.request.urlopen(url).read()
        dst_path = "results/images/people" + path
        with open(dst_path, mode="wb") as f:
            f.write(data)


def flatten(nested_list):
    return sum(nested_list, [])


def fetch_movie_detail(movie_id: int):
    movie = tmdb.Movies(movie_id)
    res = movie.info()
    print(res["title"])

    return {
        "id": res["id"],
        "title": res["title"],
        "rate": res["vote_average"],
        "genres": [g["name"] for g in res["genres"][0:2]],
        "director": fetch_director(movie),
        "casts": fetch_casts(movie),
        "reviews": fetch_reviews(movie),
        "posters": fetch_posters(movie),
    }


def fetch_director(movie):
    candidates = [c for c in movie.credits()["crew"] if c["job"] == "Director"]

    if candidates == []:
        return None

    # 1人まで
    d = candidates[0]
    movies = tmdb.People(d["id"]).movie_credits()
    d["movies"] = [c for c in movies["crew"] if c["job"] == "Director"]
    return d


def fetch_casts(movie):
    candidates = movie.credits()["cast"]

    # 2人まで
    main_casts = candidates[0 : min(2, len(candidates))]

    for cast in main_casts:
        movies = tmdb.People(cast["id"]).movie_credits()
        # 20個まで
        cast["movies"] = movies["cast"][0 : min(20, len(candidates))]

    return main_casts


def fetch_reviews(movie):
    candidates = movie.reviews()["results"]
    # 20個まで
    return candidates[0 : min(20, len(candidates))]


def fetch_posters(movie):
    candidates = movie.images()["posters"]
    # 20個まで
    posters = candidates[0 : min(20, len(candidates))]
    return [p["file_path"] for p in posters]


if __name__ == "__main__":
    # main()
    download_images()
