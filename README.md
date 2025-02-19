<h3 align="center">Translation Service</h3>

<div align="center">

[![Build Status](https://github.com/tutz/translation-service/actions/workflows/test.yml/badge.svg)](https://github.com/tutz/translation-service/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
</div>

---

<p align="center"> This project provides translation services.
  <br>
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

This project aims to provide a robust and scalable translation service that can be integrated into various applications.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

You need to have Python and pip installed on your machine.

```
sudo apt-get install python3
sudo apt-get install python3-pip
```

### Installing

A step by step series of examples that tell you how to get a development environment running.

1. Clone the repository

```
git clone https://github.com/tutz/translation-service.git
cd translation-service
```

2. Install the required packages

```
pip install -r requirements.txt
```

3. Run the server

```
python src/main.py
```

To get the language of a text:

```
curl -X 'POST' \
  'http://localhost:8000/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hello world!"
}'
```

To translate a text from German to English:

```
curl -X 'POST' \
  'http://localhost:8000/translate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hallo Welt!",
  "source_language": "de",
  "target_language": "en"
}'
```

## 🔧 Running the tests <a name = "tests"></a>

To run the automated tests for this system, use `pytest`.

### Break down into end to end tests

End to end tests ensure that the entire application flow works as expected.

```
pytest tests/end-to-end
```

### And coding style tests

Coding style tests ensure that the code adheres to the defined style guidelines using `pre-commit` hooks.

```
pre-commit run --all-files
```

## 🎈 Usage <a name="usage"></a>

To use the translation service, follow these steps:

1. Ensure the server is running by following the instructions in the [Getting Started](#getting_started) section.

2. To detect the language of a text, send a POST request to the `/detect` endpoint:

```
curl -X 'POST' \
  'http://localhost:8000/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hello world!"
}'
```

3. To translate a text from one language to another, send a POST request to the `/translate` endpoint:

```
curl -X 'POST' \
  'http://localhost:8000/translate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hallo Welt!",
  "source_language": "de",
  "target_language": "en"
}'
```

Replace `"Hallo Welt!"`, `"de"`, and `"en"` with the text you want to translate and the appropriate source and target language codes.

## 🚀 Deployment <a name = "deployment"></a>

To deploy this project on a live system using Docker and Docker Compose, follow these steps:

### Prerequisites

Ensure you have Docker and Docker Compose installed on your machine.

```
sudo apt-get install docker
sudo apt-get install docker-compose
```

### Steps

1. Clone the repository

```
git clone https://github.com/tutz/translation-service.git
cd translation-service
```

2. Build the Docker images

```
docker-compose build
```

3. Start the services

```
docker-compose up -d
```

This will start the application and its dependencies in the background.

4. Verify the services are running

```
docker-compose ps
```

You should see the translation service and its dependencies listed and running.

### Accessing the Service

The translation service will be available at `http://localhost:8000`. You can use the same `curl` commands mentioned in the [Usage](#usage) section to interact with the service.

To stop the services, run:

```
docker-compose down
```

This will stop and remove the containers, networks, and volumes created by Docker Compose.

## ⛏️ Built Using <a name = "built_using"></a>

- [FastAPI](https://fastapi.tiangolo.com/) - Web Framework
- [Uvicorn](https://www.uvicorn.org/) - ASGI Server
- [Docker](https://www.docker.com/) - Containerization
- [pytest](https://docs.pytest.org/en/stable/) - Testing Framework
- [pre-commit](https://pre-commit.com/) - Git Hook Scripts
- [mypy](http://mypy-lang.org/) - Static Type Checker
- [Ruff](https://github.com/astral-sh/ruff) - Linter


## ✍️ Authors <a name = "authors"></a>

- [@tutz](https://github.com/tutz) - Idea & Initial work
