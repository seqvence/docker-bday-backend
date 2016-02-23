#Docker Birthday Competition
##Working instructions
<br><br>
## Install Docker

Docker is available for several platforms and you may choose from any of the ones listed below:

- <a href="https://docs.docker.com/mac/step_one/">MacOS</a>
- <a href="https://docs.docker.com/linux/step_one/">Linux</a>
- <a href="https://docs.docker.com/windows/">Windows</a>

For further information please refer to the <a href="https://docs.docker.com/">Docker Docs page</a>

<br>
## Getting in the driver's seat with Docker

### Test your installation

Assuming you managed to install Docker to this point you can test your installation by running from the command line interface the following command:

	$ docker run hello-world

The output should look like

	Unable to find image 'hello-world:latest' locally
	latest: Pulling from library/hello-world
	03f4658f8b78: Pull complete 
	a3ed95caeb02: Pull complete 
	Digest: sha256:8be990ef2aeb16dbcb9271ddfe2610.......
	Status: Downloaded newer image for hello-world:latest
	
If the output the see on your screen matches the one above that means you have a working Docker installation. Congrats!

	
### Pull an image

Everything starts with an image, a docker image. In order to download it and run it on your computer you need to execute:

	$ docker pull IMAGE_NAME

First you need to know what image to pull so you can run ***docker search***. For instance, if you want to download the **latest ubuntu** image you can run the following commands:

	$ docker search ubuntu

You will retrieve all images matching the keyword **ubuntu** and now you can download the image tagged the latest by simply running the following command:

	$ docker pull ubuntu:latest

Don't believe it until you see it! 
You can check the newly downloaded image in your local repository by executing the following command:

	$ docker images

Which will have a similar output to the one below:

	REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
	ubuntu              latest              14b59d36bae0        5 days ago          187.9 MB


### Basic controlls for containers
***
#### *Run a container*
***
Since you have already an image present in your local registry let's run that one.

	$ docker run ubuntu
	$

Don't be dissapointed if you didn't get any output this time. This is due to the fact that **docker run** executes an empty command in a container.

Let's execute a command within the container, which as simple as running 

	$ docker run -i ubuntu echo 'Happy Birthday Docker!'
	$ Happy Birthday Docker!
	$

Using *-i* OPTION will execute the container in an interactive mode which allows you to see the output of the echo command.

***
#### *Check container's status*
***
You can check the status of the container created using:

	docker ps -a
	
The output will be similar to:

	CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS                           NAMES
	b49d4c8c06d2        ubuntu              "echo 'Happy Birthday"   9 seconds ago       Exited (0) 1 seconds ago                                   silly_galileo

Some useful information for going forward. In the above output please pay attention to the following columns:

Header Elements| Description
-------------  | -------------
CONTAINER ID   | Unique identifier of an instance of the image
IMAGE		     | Image name used to start the container
COMMAND        | Command which is being/was executed
STATUS         | Current status of the container

***
#### *Stop a container*
***
To stop a container, you need to execute *docker stop CONTAINER ID*

Let's give it a try, but first we need to have a running container that we can stop so we can start one.

	$ docker run -d ubuntu sleep 100
	$ f433174abbc8..................

Check the status of the container:

	$ docker ps -a
	CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS                           NAMES
	f433174abbc8        ubuntu              "sleep 100"              3 minutes ago       Up 10 seconds                                               high_blackwell
	
Container is running for 10 seconds or in your case the time indicated on the STATUS column.

	$ docker stop f433174abbc8

To check whether container is stopped now, run again:

	$ docker ps -a
	CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS                           NAMES
	f433174abbc8        ubuntu              "sleep 100"              5 minutes ago       Exited (1) 2 seconds ago                                    high_blackwell

Container is now stopped. 

If you want to stop all running containers you can use either of the commands below:

	$ docker stop $(docker ps -a -q)
	
OR

	$ docker ps -a -q | xargs docker stop

***
#### Remove a container
*** 
Should the container fulfiled its duties you can remove it by executing *docker rm*.

**Note:** Containers need to be stopped before removing them.

	$ docker rm f433174abbc8
	
Check again the status of containers and you will notice the container has been removed.

	$ docker ps -a
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	$

If you want to remove all containers you can use:

	$ docker rm $(docker ps -a -q)
	
OR

	$ docker ps -a -q | xargs docker rm
	
TIPS: For stopping and removing all containers in one line:
	
	$ docker rm $(docker stop $(docker ps -a -q))


***
#### *Getting into* containers
***
So far so good. Things are pretty straightforward, right?

Let's give it a spin and access the shell inside a container


	$ docker run -t -i ubuntu /bin/bash
	root@8d78eab8df45:/# 

Inside the container you can run any commands you would usually run on **Ubuntu Linux** so feel free to look around. 
<br>

**Note:**
Before ending the shell session you may want to install **curl** since we're planning to use it later.
This is how you do it: 
	
	root@8d78eab8df45:/# apt-get install -y curl

<br>
## Let's do some work, for real this time

### Build your own Docker image

Before you start building your own Docker image you need to get familiar to few concepts.
Docker uses a *Dockerfile* containing instructions on how to build an image. 

A full Dockerfile refence is available <a href="https://docs.docker.com/engine/reference/builder/">here</a>.

If you can't wait to build your first image you can follow the simple guide below. 

Dockerfile is structured as follows:

	# FROM is the first instruction in a Dockerfile. 
	# It specifies the image used as a base for the image which is going to be built
	FROM ubuntu:latest
	
	# MAINTAINER allows you to set the author of the image
	MAINTAINER your_name <your@email_address>
	
	# LABEL instructions add metadata to the image. 
	LABEL "My App"
	LABEL "version 1.0"
	LABEL description="This is my first app running in a Docker container" 
	
	# ENV instruction is used to set environment variables
	ENV APP_PATH /opt/app
	
	# RUN executes a command during the image building process
	RUN apt-get -y update
	RUN apt-get install -y curl
	RUN apt-get install -y git
	RUN mkdir $APP_PATH
	
	# ADD copy local/remote files to the image
	ADD ./local/app/* $APP_PATH
	
	# EXPOSE informs Docker that container listens on port 80
	EXPOSE 80


In order to build your first Docker image you can run the following command:

	$ docker build -t myapp:latest -f /path/to/dockerfile/
	$ 			...
	$ 			...
	$ Successfully built 606769c7653d
	
Once the build is over you can check your new Docker image:

	$ docker images
	REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
	myapp/latest        latest              606769c7653d        2 minutes ago       249.1 MB
	


Nevertheless, we encourage you to check the <a href="https://docs.docker.com/engine/reference/builder/">Dockerfile reference</a> to be able to build a fully capable Docker image.


## Modify Docker Voting App

### API Specs


## Build new images 
**Based on the Docker Voting App**

Writing Dockerfile

In order to build your app 

- Testing your image

## Submit new images to the DockerHub

## Submit your entry in the competition

### Submission API specs

### Check submission status