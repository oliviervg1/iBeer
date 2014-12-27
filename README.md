iBeer
=====

### How to run it
1. Git clone project.
2. Install docker.io - https://docs.docker.com/installation/.
  1. On Ubuntu 14.04 or above it should be as simple as ```sudo apt-get install docker.io```.
3. Install python-pip and python-vitualenv. These are used to run unit tests.
4. From the project root folder, run ```make run```. It might ask for your password, as docker requires sudo access.
5. Access application via [http://localhost:5001/](http://localhost:5001/).
6. Once finished, run ```make clean clean_docker``` to remove any traces.

### Features
- Search for your favourite beers thanks to BreweryDB.
- Add, rate and comment using the Python Flask backend. Uses sqlite3 to store data.
- Node.js Express frontend. Uses bootstrap for simple styling.
- Backend and frontend run in isolated Centos7 docker containers.

### Quirks
- Frontend is not tested and has poor error handling :(
- Backend is missing json schema validation.
- Currently unable to edit your ratings and comments via the UI.
