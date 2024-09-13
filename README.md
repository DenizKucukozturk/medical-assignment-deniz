# Vitestro REST API

Vitestro venipuncture device REST API written in Python using FastAPI

## Getting started

Make sure you've Python 3.10+ installed.

Setup virtual env

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Run the tests

```
python -m pytest -v
```

Start server

```
fastapi dev main.py
```

Hit the API

```
GET http://localhost:8000/collectors/{tube-id}/procedure-info
GET http://localhost:8000/procedures/{procedure-id}/collection-info
PATCH http://localhost:8000/procedures/{procedure-id}/collection-info
```


## Answers to the assignment questions

### Exercise 2a – Testing LIS integration 

- I would implement unit tests for every endpoint the API provides. Every scenario, use case, and edge case needs to be covered for effective testing.
For unit testing, I would mock the LIS component of the requests. Additionally, I would implement integration tests to assess how the endpoints
interact with the LIS. To automate these tests, I would set up GitHub Actions in our CI/CD pipeline. Whenever a new pull request is opened or
a new version of the app is deployed, GitHub Actions would run the tests and notify us with the results.


### Next steps

-  I would enhance the mock implementation of the LIS by developing it as a separate backend service. This service would include a database to simulate resources such as patients, collections, and procedures, with dedicated endpoints for Vitestro’s venipuncture device to interact with.
- Authentication is a crucial aspect of any API design. I would implement a token-based authentication system between Vitestro Cloud and Vitestro’s venipuncture device, likely using JWT with client_id and client_secret fields. A similar system would be applied between the improved LIS and the venipuncture device.
- I would containerize all backend services and the database using Docker, creating an internal network to enable seamless communication between the services. Additionally, I would automate the tests I’ve written to run every time the Docker environment is brought up via Docker Compose.
- I would improve and extend the test coverage, including tests for the newly implemented authentication systems. I would also add integration tests to validate the interaction between the newly developed LIS app and other components.


