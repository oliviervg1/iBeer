.PHONY: clean clean_docker test run base_container

clean:
	cd backend; make clean
	cd frontend; make clean

clean_docker:
	cd backend; make clean_docker
	cd frontend; make clean_docker
	- sudo docker rmi oliviervg1/centos7

test:
	cd backend; make test
	cd frontend; make test

run:
	cd backend; make run
	cd frontend; make run

run_locally:
	cd backend; make run_locally &
	cd frontend; make run_locally &

base_container:
	sudo docker build --rm -t="oliviervg1/centos7" .
