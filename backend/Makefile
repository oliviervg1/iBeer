.PHONY: clean clean_docker test build_container run

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --no-site-packages venv
	. venv/bin/activate && pip install -r requirements.txt && pip install nose mock flake8
	touch venv/bin/activate

clean:
	- rm -rf venv STATE_DIR
	- rm -rf STATE_DIR
	- find . -name "*.pyc" | xargs rm

clean_docker:
	- sudo docker stop backend
	- sudo docker rm backend
	- sudo docker rmi oliviervg1/backend

test: venv
	. venv/bin/activate && flake8 src test && nosetests -v test

build_container:
	sudo docker build --rm -q -t="oliviervg1/backend" .

run: clean clean_docker build_container
	sudo docker run --name="backend" -d -p 5000:5000 oliviervg1/backend

run_locally: venv
	. venv/bin/activate && python src/app.py
