import os
import tmdbsimple as tmdb


def main():
    print(os.environ.get("API_KEY"))


if __name__ == "__main__":
    main()
