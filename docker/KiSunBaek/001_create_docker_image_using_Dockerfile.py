# List images
docker image ls

# List all images 
docker image ls -a

# Remove image
docker image rm image_id

# Remove all images
docker image rm $(docker image ls -a -q)

# ======================================================================
# List "running" containers
docker container ls
docker ps

# List all containers
docker container ls -a

# ======================================================================
Stack: defines how services interact each service
Service: defines how containers run in the production and how containers interact other containers
Container

# ======================================================================
Portable images are defined by Dockerfile

# ======================================================================
How to define containers by Dockerfile

Dockerfile defines how environment should be configured in the container

And environments are related to resource for connecting networks,
disk drives

You also perform port mapping to connect the container to the host OS

# ======================================================================
Once you build Dockerfile, resulting in the app,
that app can run on any environments

# ======================================================================
Let's write your custom Dockerfile

mkdir docker-getting-started
touch Dockerfile

# ======================================================================
Write following contents into Dockerfile file

# You will use an official Python runtime as a parent image
FROM python:2.7-slim

# Then, you set the working directory to /app
WORKDIR /app

# And you copy the current directory contents into the container's /app directory
ADD . /app

# You install needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# You make port 80 available to connect the host OS and this container
EXPOSE 80

# You define an environment variable as NAME 
# and assign value World into that variable
ENV NAME World

# Run app.py when the container launches
CMD ["python","app.py"]

# ======================================================================
Let's create app.py and requirements.txt in the same directory where Dockerfile is located

touch requirements.txt
Flask
Redis

# ======================================================================
touch app.py

from flask import Flask
from redis import Redis, RedisError
import os
import socket

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

# From app, if routing comes through "/", execute hello()
@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis server to count</i>"

    # value of environment variable NAME in the container will be into {name}
    html = "<h3>Hello {name}!</h3>\n" \
           "<b>Hostname:</b> {hostname}<br/>\n" \
           "<b>Visits:</b> {visits}\n"

    return html.format(name=os.getenv("NAME","world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

# ======================================================================
Let's build Dockerfile into app

# -t option can be used for specifying container name
# . means location where files which are needed for building are located in
# Created image (container?) will be into docker system
docker build -t hellopy .

# ======================================================================
# Check whether you could get hellopy image

docker image ls

# ======================================================================
# -p option is for port mapping
# -p host_port:container_port
# hellopy: image name
# This will create a container for hellopy image
# and that container gets started
docker run -p 4000:80 hellopy

# ======================================================================
# Check
https://localhost:4000

# ======================================================================
To exit from the container, press ctrl+c

# ======================================================================
Let's run the container in detached mode (background mode or daemon mode)

docker run -d -p 4000:80 hellopy

Since it runs in background, you can type in terminal

# ======================================================================
# List container
docker container ls

# ======================================================================
# To stop container,
docker container stop container_hash_id

# To enforce shutdown container
docker container kill container_hash_id

# To remove container
docker container rm container_hash_id

# To remove all containers
docker container rm $(docker container ls -a -q)

# ======================================================================
You can share your custom image onto web

# ======================================================================
Registry is the collection of Repositories

Repositories is the collection of images 

Repositories of github have projects

Repositories of Dockerhub have images(?)

# ======================================================================
# Login your account to publish your image onto Dockerhub
docker login

# ======================================================================
Tag the image

Naming rule is username/repository:tag

tag is optional but recommended
because one image can have multiple versions

# ======================================================================
docker tag hellopy your_user_name/hellopy:0.0.1

docker image ls

you should see added your_user_name/hellopy into the list of your images

This process is almost same with tagging on github

# ======================================================================
# Upload your image
docker push your_user_name/hellopy:0.0.1

# ======================================================================
Pull the image you just uploaded from the local terminal

docker run -p 4000:80 your_user_name/hellopy:0.0.1

https://localhost:4000

# ======================================================================
