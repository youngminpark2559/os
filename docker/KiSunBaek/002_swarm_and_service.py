# ======================================================================
In this lecture, you will see about "docker compose", "docker service", "docker swarm"

# ======================================================================
Install docker compose

# ======================================================================
Stack
Service (you will learn here)
Container (you have learned this from last lecture)

# ======================================================================
In a distributed application, 
different pieces of the app are callled "services"

Suppose a web site where people share videos

That web site (web application) will have "database service", 
"encoding videos in background service", "front-end service"

A service can be considered as a container in docker

# ======================================================================
One container could run one image 

but if you codify the way that images run;
about what ports image should use, how many containers image requires,
how many resources (CPU, disk) image needs

Scaling a service is to change the number of container instances running that piece of software,
and scaling is to assign more resources to that service.

# ======================================================================
In docker, above "codify" and "scaling" are easy
by using docker-compose.yml (YAML file) file

docker-compose.yml defines how docker containers should run in the production environment

# ======================================================================
Save this file as docker-compose.yml file name wherever you want. 

version: "3"
services:
  # Name of this service is "web"
  web:
    # replace username/repo:tag with your name and image details
    # like your_user_name/hellopy:0.0.1
    # You let docker to know what image it should pull
    image: username/repo:tag
    deploy:
      # You use 5 container instances for your_user_name/hellopy:0.0.1 image
      replicas: 5
      resources:
        limits:
          # 5 containers use 10% of CPU 
          cpus: "0.1"
          # 5 containers use 50M of RAM
          memory: 50M
      # you will restart containers
      restart_policy:
         # if you run into failure
        condition: on-failure
    # Host port:container port
    # 5 containers share 80 port via load-balanced network call
    # In other words, all 5 containers use 80 port 
    # which is mapped to 4000 port of host computer
    ports:
      - "4000:80"
    # load-balanced network which suppies above "port functionality"
    networks:
      # is webnet
      # It's like multitasking on single thread to use multiple ports? 
      # This references following webnet
      - webnet
networks:
  webnet:

# ======================================================================
Before you use 
docker stack deploy
you first use 
docker swarm init

# ======================================================================
# After 
docker swarm init
# Use this
# getstartedlab is service name you will create
docker stack deploy -c docker-compose.yml getstartedlab

# ======================================================================
Check service
docker service ls

then you will see created service
# Name of this service is "web"
getstartedlab_web

# ======================================================================
Single service stack runs 5 container instances  

# ======================================================================
5 containers which are running in the getstartedlab_web service are called "Tasks"

Tasks are given unique IDs which are numerically increment

docker service ps getstartedlab_web
you will see
1,2,3,... are Tasks
getstartedlab_web.1
getstartedlab_web.2
getstartedlab_web.3
getstartedlab_web.4
getstartedlab_web.5

# ======================================================================
https://localhost:8000

Every time you refresh web page, Hostname (continer ID) changes

# ======================================================================
Let's scale the app

You can manipulate the value of "replicas" in docker-compose.yml file

version: "3"
services:
  # Name of this service is "web"
  web:
    # replace username/repo:tag with your name and image details
    # like your_user_name/hellopy:0.0.1
    # You let docker to know what image it should pull
    image: username/repo:tag
    deploy:
      # You use 7 container instances for your_user_name/hellopy:0.0.1 image
      # You change this from 5 to 7
      replicas: 7
      resources:
        limits:
          # 7 containers use 10% of CPU 
          cpus: "0.1"
          # 7 containers use 50M of RAM
          memory: 50M
      # you will restart containers
      restart_policy:
         # if you run into failure
        condition: on-failure
    # Host port:container port
    # 7 containers share 80 port via load-balanced network call
    # In other words, all 7 containers use 80 port 
    # which is mapped to 4000 port of host computer
    ports:
      - "4000:80"
    # load-balanced network which suppies above "port functionality"
    networks:
      # is webnet
      # It's like multitasking on single thread to use multiple ports? 
      # This references following webnet
      - webnet
networks:
  webnet:

# ======================================================================
docker stack deploy -c docker-compose.yml getstartedlab
You will see updated service

docker service ps getstartedlab_web
You will see 7 services

docker container ls
You will see 7 images (your_user_name/hellopy:0.0.1) running on 7 containers

# ======================================================================
docker stack rm getstartedlab
You will see 
Removing service getstartedlab_web
Removing service getstartedlab_webnet

# ======================================================================
# since you did docker swarm init, you will leave from it
docker swarm leave --force

# ======================================================================
Let's see docker swarm

docker-compose.yml file defines how the app (app.py) should run like following

version: "3"
services:
  # What service you use 
  web:
    image: username/repo:tag
    deploy:
      # How many replicas you will use
      replicas: 7
      # How much of resources you will use
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
      restart_policy:
         # if you run into failure
        condition: on-failure
    # How you will perform the port mapping
    ports:
      - "4000:80"
    # What network will you use
    networks:
      - webnet
networks:
  webnet:

# ======================================================================
You will deploy this app (app.py) onto a cluster

In other words, you will run that app on multiple machines.

Multiple container and multiple machine applications are possible 
by joining multiple machines into a "Dockernized" cluster called a swarm

# ======================================================================
A swarm is a group of machines 
which are running Docker and are joined into a cluster.

You can use Docker commands to swarm manager

Machines can be virtual machine or physical machine.

After machines join the swarm, each machine is called as "node"

# ======================================================================
Swarm manager has serveral strategies how to run multiple containers.


If swarm manager uses "emptiest node strategy",
swarm manager uses minimal number of machines to run the container.

For example, suppose you have 3 machines,
and you have 6 containers you need to run.

If one machine can run 6 containers, 
you will use one machine in "emptiest node strategy" of the swarm manage.

# ======================================================================
If swarm manager uses "global strategy",
swarm manager uses one machine per each container.

For example, suppose you have 3 machines,
and you have 6 containers you need to run.

If each machine must run over-one-container,
like 1-1-4, 2-2-2, 3-1-2 patterns.

# ======================================================================
Swarm managers are machines which can execute your commands,
can authoize other machines to join the swarm as workers (in other words, nodes?).

Workers are to provide capacity 
and workers don't have the authority to tell any other machine wha it can and cannot do

# ======================================================================
So far, you have used Docker on the single host (your local computer)

But docker can change to "swarm mode"
by using docker swarm init

Then, current machine becomes "swarm manager".

# ======================================================================
Then, commands are executed by "swarm manager" than "current machine"

# ======================================================================
If you type following command on other machine, that machine will join the swarm
with supplying additional information to join the machine which has swarm manager.
docker swarm join

# ======================================================================
Let's create multiple virtual machines using virtualbox

docker-machine create -driver virtualbox myvm1
docker-machine create -driver virtualbox myvm2

Check created machines
docker-machine ls

# ======================================================================
Let's start virtual machines

docker-machine start myvm1
docker-machine start myvm2

# ======================================================================
Let's check started machines
docker-machine ls

# ======================================================================
You will make first virtual machine as "swarm manage machine"
which can execute commands which are related to management

The other one will become "worker".

# ======================================================================
Let's see IP address of each machine
docker-machine ls

docker-machine ssh myvm1 "docker swarm inin --advertise-addr 192.111.11.111"

# ======================================================================
To add a worker to this swarm,
give the following command to myvm2

docker-machine ssh myvm2 "docker-swarm join --token SMTXX-1-ffiejfef9876 192.111.11.222"

# ======================================================================
docker-machine ssh myvm1 "docker node ls"

ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
brtu9urxwfd5j0zrmkubhpkbd     myvm2               Ready               Active
rihwohkh3ph38fhillhhb84sk *   myvm1               Ready               Active              Leader

# ======================================================================
To leave swarm, 
docker-machine ssh myvm2 "docker-swarm leave"

# ======================================================================
Now, VM doesn't have docker-compose.yml file to configure environment

To do similar thing, 
you need to connect the current shell of your PC and the swarm manager of myvm1

# ======================================================================
Run the following to get the command to configure your shell to talk to myvm1.
docker-machine env myvm1

You will get this
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/sam/.docker/machine/machines/myvm1"
export DOCKER_MACHINE_NAME="myvm1"
# Run this command to configure your shell:
# eval $(docker-machine env myvm1)

# ======================================================================
Run the following 
eval $(docker-machine env myvm1)

# ======================================================================
Run 
docker-machine ls

# ======================================================================
Now, you can use your current shell as if you're in myvm1
in other worlds, you don't need to use ssh from local PC

# ======================================================================
docker note ls

# ======================================================================
You can still use all files in your local PC, 
including docker-compose.yml file

docker stack deploy -c docker-compose.ymb getstartedlab
It means you deploy app

# ======================================================================
docker stack ps getstartedlab
ID            NAME                  IMAGE                     NODE   DESIRED STATE
jq2g3qp8nzwx  getstartedlab_web.1   gordon/get-started:part2  myvm1  Running
88wgshobzoxl  getstartedlab_web.2   gordon/get-started:part2  myvm2  Running
vbb1qbkb0o2z  getstartedlab_web.3   gordon/get-started:part2  myvm2  Running
ghii74p9budx  getstartedlab_web.4   gordon/get-started:part2  myvm1  Running
0prmarhavs87  getstartedlab_web.5   gordon/get-started:part2  myvm2  Running

# ======================================================================
Instead of entering myvm1,
you still use ssh way in some cases

docker-machine ssh <machine> "<command>"

You can use scp to transfer files across machines
docker-machine scp <file> <machine>:~

# ======================================================================
Copy ID and paste it onto browser

192.111.111.111
192.111.111.222

# ======================================================================
The network you created is shared between workers, 
and load-balancing is also possible.

# ======================================================================
# /home/young/Pictures/2019_02_23_10:10:51.png

192.168.99.100: IP of worker
8080: port

Every nodes are connected to each other.

# ======================================================================
Let's edit docker-compose.yml file

version: "3"
services:
  web:
    image: username/repo:tag
    deploy:
      replicas: 4
      resources:
        limits:
          cpus: "0.1"
          memory: 50M
      restart_policy:
        condition: on-failure
    ports:
      - "4000:80"
    networks:
      - webnet
networks:
  webnet:

And deploy 
docker stack deploy -c docker-compose.ymb getstartedlab

# ======================================================================
docker stack ps getstartedlab

# ======================================================================
You can pull down stacks
docker stack rm getstartedlab

# ======================================================================
You make myvm2 leave from swarm
docker-machine ssh myvm2 "docker swarm leave"

# You make myvm1 leave from swarm 
# but it should be force because myvm1 is swarm manager
docker-machine ssh myvm1 "docker swarm leave --force"

# ======================================================================
Now, docker-machine is being attached to myvm1

To release your current shell from myvm1,
eval $(docker-machine evn -u)

# ======================================================================
See list of machines
docker-machine ls

Stops machines
docker-machine stop myvm1
docker-machine stop myvm2

# ======================================================================
