# Deploy Python app To Openshift

The purpose of this repo is to demonstrate the steps involved in deploying a FastAPI-powered python application to OpenShift. Openshift is Red Hat's enterprise version of Kubernetes, and is the platform used for container orchestration on Osprey, Hartree's own on-premise cloud. The source code for our test app is available in this repo, along with a Dockerfile to containerise the application. 

The app is based on a simple in-memory database management system written in Python, where users can perform CRUD operations through the FastAPI swagger page which resolves to http://localhost:8080/docs. 

The steps to build the container image, initially locally, and then deploy to run on OpenShift, are explained below. These instructions can be used as a template guide for deploying more sophisticated applications to Openshift, either directly from existing gitlab repositories, or via container images uplaoded to STFC's Harbor registry. 


### Build container image and test locally

The instructions below assume you have the docker command line tools installed on your local machine. The CLI is provided through Docker Desktop, but this is no longer free for organisations that employ over 250 people. Instead, an alternative is to use the open-source [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation/), a drop-in replacement for Docker Desktop. 

1) Clone this repository, and from the top-level directory, build a container image from the supplied Dockerfile by running the command `docker build -t my-fastapi-test .`

2) Run a container based on the image as follows: `docker run -d --name fastapi_container -p 8080:8080 my-fastapi-test`

3) Go to a web browser on your host machine and check you can access the swagger-ui page by navigating to `http://127.0.0.1:8080/docs` (or `localhost:8080/docs`)


### Deploy to Openshift

The [wiki page](https://gitlab.stfc.ac.uk/ywg45244/deploy-python-to-openshift/-/wikis/home) for this repository describes how our test app can be deployed to an Openshift cluster via the Openshift command line interface (CLI). Instructions for installing the CLI via the Openshift web console can be found [here](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html). Access to the Openshift web console on Osprey is provided through [SAFE](https://um.hartree.stfc.ac.uk) on a project-by-project basis, alternatively it is possible to sign up for an Openshift sandbox developer account (see https://developers.redhat.com/developer-sandbox) which provides access to a modest Openshift cluster for 30 days free of charge, and is an ideal test-bed for general upskilling purposes. 








