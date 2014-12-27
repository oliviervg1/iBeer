.PHONY: clean clean_docker test build_container run

clean:
	- rm -rf node_modules

clean_docker:
	- sudo docker stop frontend
	- sudo docker rm frontend
	- sudo docker rmi oliviervg1/frontend

test:
	

build_container:
	sudo docker build --rm -q -t="oliviervg1/frontend" .

run: clean clean_docker test build_container
	sudo docker run --name="frontend" --link backend:backend -d -p 5001:5001 oliviervg1/frontend

run_locally:
	npm install
	cd src; nodejs server.js
