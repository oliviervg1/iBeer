env: env/bin/activate

env/bin/activate: requirements.txt
	test -d env || virtualenv -p python3 env
	. env/bin/activate && pip install -r requirements.txt && pip install nose mock flake8

.PHONY: clean
clean:
	- rm -rf env STATE_DIR
	- rm -rf STATE_DIR
	- find . -name "*.pyc" | xargs rm

.PHONY: test
test: env
	. env/bin/activate && flake8 src test && nosetests -v test

.PHONY: run
run: env
	. env/bin/activate && python src/app.py
