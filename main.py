import os
import json
import tmdbsimple as tmdb


def main():
    tmdb.API_KEY = os.environ.get("API_KEY")
    target_movie_ids = [
        447404,  # Detective Pikachu
        299534,  # Avengers Endgame
        118,  # Charlie and the Chocolate Factory
        109445,  # Frozen
        335984,  # Blade Runner 2049 (because we already have a poster, it is easy to show demo for visitor)
        315011,  # Shin Godzilla
    ]

    movies = [fetch_movie_detail(movie_id) for movie_id in target_movie_ids]

    with open("results/result.json", "w") as f:
        json.dump(movies, f, indent=4)


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


if __name__ == "__main__":
    main()
