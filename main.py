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

    final_result = {}

    final_result["title"] = [
        fetch_movie_detail(movie_id) for movie_id in target_movie_ids
    ]

    with open("results/result.json", "w") as f:
        json.dump(final_result, f)


def fetch_movie_detail(movie_id: int):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    return movie.title


if __name__ == "__main__":
    main()
