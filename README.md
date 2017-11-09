Quick README
============

Create venv

	virtualenv -p python3 --no-site-packages venv
	. venv/bin/activate
	pip install -r requirements.txt

Installation

	cd maplecrofttweets
	./manage.py migrate
	# Import countries into database
	./manage.py importcsv --filename ../countries.csv
	./manage.py runserver 0:8881

For admin access

	./manage.py createsuperuser

Web access

	http://127.0.0.1:8881/tweets/
