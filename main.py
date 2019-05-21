import os
import json
import urllib
import time
import tmdbsimple as tmdb

# 指定されたMovie IDの詳細をまるっと取得して一つのJSONにする
def fetch_information():
    json_filepath = "results/result.json"
    key = os.environ.get("API_KEY")

    if key is None:
        raise Exception("Please set your API KEY in .env file ")

    tmdb.API_KEY = key
    target_movie_ids = [
        447404,  # Detective Pikachu
        299534,  # Avengers Endgame
        335984,  # Blade Runner 2049 (because we already have a poster, it is easy to show demo for visitor)
        157336,  # Interstellar
        207703,  # Kingsman
        299537,  # Captain Marvel
        324857,  # Spider Verse
        # 109445,  # Frozen
        # 315011,  # Shin Godzilla
        # 118,  # Charlie and the Chocolate Factory
        # 180,  # Minority Report
        # 105,  # Back to the future
        # 27205,  # Inception
    ]

    movies = [fetch_movie_detail(movie_id) for movie_id in target_movie_ids]

    with open(json_filepath, "w") as f:
        json.dump(movies, f, indent=4)


# 保存されているJSONをパースして必要な画像をすべてダウンロードする
def download_images():
    target_filepath = "results/result.json"
    image_base = "https://image.tmdb.org/t/p/w1280"
    tmdb.API_KEY = os.environ.get("API_KEY")

    with open(target_filepath, "r") as f:
        movies = json.loads(f.read())

    for m in movies:
        print(f'{m["title"]}: {len(m["reviews"])} Reviews')

    directors = [m["director"] for m in movies]
    casts = flatten([m["casts"] for m in movies])
    people = directors + casts

    movies_of_people = flatten([p["movies"] for p in people])
    posters_of_people = [m["poster_path"] for m in movies_of_people]
    posters_of_movies = flatten([m["posters"] for m in movies])

    portraits = compact([c["profile_path"] for c in people])
    posters = compact(posters_of_movies + posters_of_people)

    for (directory, filenames) in [("people", portraits), ("posters", posters)]:
        os.makedirs(f"results/images/{directory}", exist_ok=True)
        for filename in filenames:
            time.sleep(0.2)
            url = image_base + filename
            print(url)
            dst_path = f"results/images/{directory}/{filename}"
            data = urllib.request.urlopen(url).read()
            with open(dst_path, mode="wb") as f:
                f.write(data)


def flatten(nested_list):
    return sum(nested_list, [])


def compact(none_containing_list):
    return [item for item in none_containing_list if item is not None]


def fetch_movie_detail(movie_id: int):
    movie = tmdb.Movies(movie_id)
    res = movie.info()
    print(res["title"])

    return {
        **res,
        **{
            "director": fetch_director(movie),
            "casts": fetch_casts(movie),
            "reviews": fetch_reviews(movie),
            "posters": fetch_posters(movie),
        },
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
    fetch_information()
    download_images()
