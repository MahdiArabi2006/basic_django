# Asynchronous Infrastructure & Microservices Blueprint

A clean, production-grade template designed to implement and demonstrate core principles of distributed backend architectures, asynchronous job queuing, and DevOps orchestration.

## Project Philosophy
This repository does not focus on complex frontend layouts or specific monolithic business use-cases. Instead, **the primary goal of this project is to serve as an architectural sandbox for integrating infrastructure components**—proving how modern web applications decouple stateless client authentication, handle heavy non-blocking background operations, and manage secure production-grade reverse proxy networks.

---

## Core Architecture & System Features

The application showcases a standard multi-service ecosystem where workloads are segmented effectively between synchronous API routing and asynchronous background threads:

* **Decoupled REST API Backend:** Powered by Django and Django REST Framework (DRF) to process stateless operations.
* **Stateless Authentication Engine:** High-security user session handling using JSON Web Tokens (JWT).
* **Asynchronous Execution Queue:** Heavy/long-running operations are instantly offloaded into background processes via Celery, maintaining a sub-second API response time.
* **In-Memory Message Broker:** Utilizes Redis for high-throughput communication and state management between the API server and worker nodes.
* **Production Ingress Layer:** Configured with Nginx acting as an edge reverse proxy and Gunicorn as the WSGI server to manage production traffic, static assets, and upstream routing.
* **Multi-Container Orchestration:** 100% containerized network environment bundled using Docker and Docker Compose for instant, reproducible deployments.

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
