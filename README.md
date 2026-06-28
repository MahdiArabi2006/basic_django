# Django Asynchronous Web Architecture

A clean implementation of a web backend focused on integrating asynchronous task queues, state management, and containerized deployment.

## Project Philosophy
The main goal of this repository is to demonstrate the practical integration of essential backend infrastructure tools. It avoids complex business logic or advanced frontend design, focusing purely on setting up a correct production-ready pipeline.

---

## Core Architecture & System Features

* **REST API:** Built with Django and Django REST Framework (DRF).
* **Session Management:** Stateless user authentication using JSON Web Tokens (JWT).
* **Background Workers:** Non-blocking asynchronous task execution using Celery.
* **Message Broker:** Redis for handling communication between Django and Celery.
* **Web Server & Proxy:** Gunicorn as the WSGI server, with Nginx acting as a reverse proxy.
* **Containerization:** Environment orchestration via Docker and Docker Compose.
---

## Tech Stack

* **Backend Framework:** Python, Django, Django REST Framework
* **Asynchronous Engine:** Celery, Redis
* **DevOps & Ingress:** Docker, Docker Compose, Nginx, Gunicorn
* **Frontend Stub:** Vue.js, JavaScript

---

## Getting Started

### Prerequisites
* Docker and Docker Compose installed.

### Spin up the Stack

You can launch the entire ecosystem (API, Frontend, Redis, Celery, and Nginx) with a single command:

1. Clone the repository:
   ```bash
   git clone [https://github.com/MahdiArabi2006/basic_django.git](https://github.com/MahdiArabi2006/basic_django.git)
   cd basic_django
   docker-compose up --build
