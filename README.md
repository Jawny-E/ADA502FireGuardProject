# ADA502FireGuardProject

## Getting started
This project is still under heavy development, and while functional there is no claim that this follows the best practices for security. Anyways, to run the project in it's current state.
1. Clone the repository
2. Edit the values in the .env file, especially mongo_db relies on external services
3. Run the Docker compose, everything should work out of the box as long as the environment varibles are correct

You may note that even though the compose includes keycloak and postgresql for persistent storage, these have not been implemented as part of the API yet. We are on it! There was some issues with creating preset settings for keycloak and using python to connect to keycloak. We expect to have this over the weekend, and will update the README as we go along

## Architecture
This project is setup as containerized services orchastrated through tools such as Docker-Compose or Kubernetes. The following services are planned:
- API connectionpoint
- KeyCloak with database for persistent storage
- Database for FireGuard data (external) 
- Messaging service

## API structure
