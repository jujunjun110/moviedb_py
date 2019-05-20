import os
import tmdbsimple as tmdb


def main():
    target_movie_ids = [
        447404,  # Detective Pikachu
        299534,  # Avengers Endgame
        118,  # Charlie and the Chocolate Factory
        109445,  # Frozen
        335984,  # Blade Runner 2049 (because we already have a poster, it is easy to show demo for visitor)
        315011,  # Shin Godzilla
    ]

    tmdb.API_KEY = os.environ.get("API_KEY")
    for movie_id in target_movie_ids:
        movie = tmdb.Movies(movie_id)
        response = movie.info()
        print(movie.title)


if __name__ == "__main__":
    main()
