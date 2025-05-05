<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Introduction](#introduction)
   * [Getting started](#getting-started)
      + [Prerequisites](#prerequisites)
      + [Getting started](#getting-started-1)
      + [Accessing the API](#accessing-the-api)
         - [Authentication](#authentication)
   * [Background](#background)
      + [Overall Architecture](#overall-architecture)
      + [Techonolgies applied](#techonolgies-applied)
      + [API/Business Logic](#api-structure)
      + [Databases](#databases)
      + [Messaging System](#messaging-system)
      + [Authentication and Authorization](#authentication-and-authorization)
      + [CI/CD and package control](#cicd-and-package-control)

<!-- TOC end -->

<!-- TOC --><a name="introduction"></a>
# Introduction
This repository is a project completed as part of the ADA502 - Cloud Computing course at HVL, and encompasses creating a REST API interface for getting firerisk with the [FRCM python library](https://pypi.org/project/dynamic-frcm/). 

<!-- TOC --><a name="getting-started"></a>
## Getting started
<!-- TOC --><a name="prerequisites"></a>
### Prerequisites
This approach to running the project is based on you having access to the following technolgies in your environment: git, Docker-Desktop, DockerHub and Postman. You can use similar techonolgies as alternatives if you would like. The project has been tested against the recommended technolgies and we highly recommend them for beginners.


<!-- TOC --><a name="getting-started-1"></a>
### Getting started
This project is the result of an assignment for creating a API for calculating firerisk in areas of Norway, and should be considered a result of learning and testing new techonologies.  
The project is still undergoing changes and can be considered a v0 for further development.  
To run the project in it's current state you can do the following:
1. Clone this repository
2. Edit the values in the .env file to match your setup. Take especially note of the values related to the MongoDB
3. Run all the services in the Docker compose using `docker-compose up -d`, all containers should run locally out of the box 

<!-- TOC --><a name="accessing-the-api"></a>
### Accessing the API
In your webrowser you can now access the public URLs exposed by the API. Since the API is built upon FastAPI one of these is localhost:8000/docs where all endpoints are detailed. Currently the following are available:
| Endpoint                             	| Authentication 	|
|--------------------------------------	|----------------	|
| localhost:8000/                      	| None           	|
| localhost:8000/public                	| None           	|
| localhost:8000/docs                  	| None           	|
| localhost:8000/api                   	| Token          	|
| localhost:8000/api/{location}        	| Token          	|
| localhost:8000/api/{location}/trends 	| Token          	|

<!-- TOC --><a name="authentication"></a>
#### Authentication
To access the endpoints requiring authentication you need a JWT-token aquired from Keycloak. To do this you need to send a POST-request to http://localhost:8080/realms/FireGuard/protocol/openid-connect/token. With the following parameters in the body of the HTTP-request (note also that the body has x-www-form-urlencoded):
| **Key**    	| **Content**                     	| **Test Value** 	|
|------------	|---------------------------------	|----------------	|
| client_id  	| ClientID registered in Keycloak 	| FireGuardAPI   	|
| username   	| User in keycloak database         | test           	|
| password   	| Password for user               	| testing        	|
| grant_type 	| Type of authentication          	| password       	|


*Using the provisioned test-user in Postman looks like this:*
![image](https://github.com/user-attachments/assets/1d840207-bdef-4a7c-ad25-f0eb2f7c5759)

From the POST-request will get the access-token in the response-body. To access endpoints protected by the API you can now send GET-requests to any API with this access token in the body. The figure below shows this completed for the endpoint localhost:8000/api/bergen in Postman. If everything is set up correctly you should get firerisk predictions in the response
![image](https://github.com/user-attachments/assets/82079123-d36d-4c9c-a44d-31f6079a0239)


The token does have a timeout, and you will have to get a new token each time this happens. Just repeat the earlier steps and replace your old token with the new one. 


<!-- TOC --><a name="background"></a>
## Background

<!-- TOC --><a name="overall-architecture"></a>
### Overall Architecture
This project is setup as containerized services orchastrated through tools such as Docker-Compose or Kubernetes. The following services are planned:
- API connectionpoint
- KeyCloak with database for persistent storage
- Database for FireGuard data (external) 
- Messaging service

<!-- TOC --><a name="techonolgies-applied"></a>
### Techonolgies applied
- Python -> Poetry package manager
- Docker -> Composes and images
- Keycloak
- HiveMQ Cloud
- MongoDB
- PostgreSQL
- GitHub/GitHub Actions


<!-- TOC --><a name="api-structure"></a>
### API/Business Logic
- REST API

<!-- TOC --><a name="databases"></a>
### Databases

<!-- TOC --><a name="messaging-system"></a>
### Messaging System

<!-- TOC --><a name="authentication-and-authorization"></a>
### Authentication and Authorization

<!-- TOC --><a name="cicd-and-package-control"></a>
### CI/CD and package control
