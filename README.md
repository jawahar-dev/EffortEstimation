#clone the repo

git clone https://github.com/jawahar-dev/EffortEstimation.git

#goto project folder and create virtual environment, and activate it

python -m venv venv

cd venv/scrips

.activate

#install required packages using pip

pip install -r requirements.txt

#run the application using

python app.py

#open the server in web browser

http://localhost:5000 


#run testst for the application using PyTest

python -m pytest

#using the application in Docker environment using docker-compose

#install docker, docker-compose in the machine, and execute below commands

docker-compose build

docker compose up