# **Django App Kubernetes Deployment**

This project demonstrates how to deploy a Django application with PostgreSQL using **Kubernetes**. The application is Dockerized and can be easily scaled and managed through Kubernetes resources.

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Pre-requisites](#pre-requisites)
3. [Setup Instructions](#setup-instructions)
    - [1. Dockerize the Application](#1-dockerize-the-application)
    - [2. Build and Push Docker Image](#2-build-and-push-docker-image)
    - [3. Kubernetes Configuration](#3-kubernetes-configuration)
4. [Kubernetes Resources](#kubernetes-resources)
    - [a. Django Deployment](#a-django-deployment)
    - [b. PostgreSQL Deployment](#b-postgresql-deployment)
    - [c. Services and Ingress](#c-services-and-ingress)
    - [d. Persistent Volume for PostgreSQL](#d-persistent-volume-for-postgresql)
5. [Running Migrations and Creating Superuser](#running-migrations-and-creating-superuser)
6. [Accessing the Application](#accessing-the-application)
7. [Monitoring and Scaling](#monitoring-and-scaling)
8. [Troubleshooting](#troubleshooting)

---

## **Project Overview**

This project includes:

- **Django**: The Python web framework used for the application.
- **PostgreSQL**: The relational database used for the app.
- **Kubernetes**: The orchestration platform to manage and scale the application.
- **Docker**: Containerization platform to package the application.
- **Ingress**: For exposing the app to the outside world through a domain name.

---

## **Pre-requisites**

To successfully deploy this project, you will need the following:

- **Docker**: Installed on your local machine.
- **Kubernetes Cluster**: Set up either locally (e.g., using `minikube`) or on a cloud platform (e.g., AWS, GCP, etc.).
- **kubectl**: Kubernetes command-line tool to interact with the cluster.
- **Docker Hub or Container Registry**: To push your Docker image.

---

## **Setup Instructions**

### **1. Dockerize the Application**

The application is Dockerized using a `Dockerfile`. Create a `Dockerfile` in the root of your project:

```Dockerfile
# Dockerfile

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


---

## **Architecture Diagram**
+------------------------------------------------------------+
|                        Users                               |
|                                                            |
|  +------------------+          +------------------+        |
|  |  Browser/API      |          |  Browser/API      |       |
|  +------------------+          +------------------+        |
|                                                            |
+-----------------------------|------------------------------+
                              |
                              v
+-----------------------------v------------------------------+
|                         Ingress                             |
|    (Exposes Django service via HTTP/HTTPS)                  |
|-------------------------------------------------------------|
                              |
                              v
+------------------+    +-----------------------------+       |
|   ConfigMap      |    |            Secrets           |       |
+------------------+    +-----------------------------+       |
           |                          |                        |
           v                          v                        |
+------------------+    +-----------------------------+        |
|   Django Pod     |    |         PostgreSQL Pod       |        |
| +--------------+ |    |  +-----------------------+   |        |
| |  Django App  | |    |  | PostgreSQL Database    |   |        |
| | (Python &    | |    |  |                       |   |        |
| |  Gunicorn)   | |    |  |                       |   |        |
| +--------------+ |    |  +-----------------------+   |        |
|      ReplicaSet  |    |          ReplicaSet         |        |
+------------------+    +-----------------------------+        |
        |                           |                         |
        v                           v                         |
+------------------+       +------------------------------+    |
|  Persistent Vol  |       |       Persistent Vol         |    |
| (for PostgreSQL) |       |  (Optional for Django logs)  |    |
+------------------+       +------------------------------+    |

