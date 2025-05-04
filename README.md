# ADA502FireGuardProject

## Prerequisites
Before you run this project you need: 
Docker
Postman


## Getting started
This project is still under heavy development, and while functional there is no claim that this follows the best practices for security. Anyways, to run the project in it's current state.
1. Clone the repository
2. Edit the values in the .env file, especially mongo_db relies on external services
3. Run the Docker compose, everything should work out of the box as long as the environment varibles are correct

## Accessing the API
In your webrowser you can now access localhost:8000/ and localhost:8000/public. All other URL's require authentication for access. This can be done several ways, but we have opted to use postman. 
In postman open a new tab. In this new tab, choose POST and use this link http://localhost:8080/realms/FireGuard/protocol/openid-connect/token. You also have to provide some information for the body. Choose "body" underneath the link you just posted and check off the x-www-form-urlencoded. 
In your body you need : 
client_id
username
password
grant_type

which has to match a user in the database. For demonstration purposes we have created a test user that can be used, which you will find in the picture. Your tab in postman should now look something like this: 
![image](https://github.com/user-attachments/assets/1d840207-bdef-4a7c-ad25-f0eb2f7c5759)

Click send and you should get a response including a token. Copy your token and head over to a new tab in postman. Go to Authorization (whichs you will find on the same line as body) and choose the Bearer token. Paste your token, write the URL you want (for eks. localhost:8000/api/bergen) and click post. If you have done everything right you will now get the firerisks in Bergen. 
![image](https://github.com/user-attachments/assets/82079123-d36d-4c9c-a44d-31f6079a0239)


The token do have a timeout, and you will have to get a new token each time this happens. Just repeat the earlier steps and replace your old token with the new one. 

Possible URL's at this point in time is: 
localhost:8000/
localhost:8000/public
localhost:8000/api
localhost:8000/api/{location}
localhost:8000/api/{location}/trends


## Architecture
This project is setup as containerized services orchastrated through tools such as Docker-Compose or Kubernetes. The following services are planned:
- API connectionpoint
- KeyCloak with database for persistent storage
- Database for FireGuard data (external) 
- Messaging service

## API structure
