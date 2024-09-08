install:
	pip install -r requirements.txt

run:
	python app.py

npm:
	cd client && npm install

frontrun:
	cd client && npm start

test:
	python test_api.py
