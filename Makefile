setup:
	PIPENV_VENV_IN_PROJECT=TRUE pipenv install

run:
	make fetch_info
	make download_images

fetch_info:
	pipenv run python -c 'import main; main.fetch_information()'

download_images:
	pipenv run python -c 'import main; main.download_images()'
