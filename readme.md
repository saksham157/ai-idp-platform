# AI-IDP Platform

## Overview

AI-IDP Platform is a cloud-native Internal Developer Platform (IDP) designed to automate service onboarding, CI/CD generation, GitOps deployment workflows, and developer experience using Kubernetes, Jenkins Shared Libraries, ArgoCD, PostgreSQL, and dynamic build agents.

The goal of this project is to simulate how modern platform engineering teams build centralized developer platforms that reduce manual DevOps work for developers.

Instead of every team maintaining separate CI/CD pipelines and deployment logic, this platform centralizes automation and standardizes workflows.

---

# Problem Statement

In many organizations:

- Every repository contains different Jenkins pipelines
- CI/CD logic becomes duplicated
- Developers manually configure deployments
- Kubernetes manifests become inconsistent
- Security and deployment standards vary between teams
- Platform teams struggle to maintain standardization

AI-IDP Platform solves this by introducing:

- Shared CI/CD pipelines
- Metadata-driven onboarding
- Dynamic build agents
- GitOps deployment workflows
- Centralized platform automation

---

# Platform Architecture

```text
Developer Repository
        │
        │ platform.yaml
        ▼
Jenkins Shared Library
(platform-shared-library)
        │
        ▼
Dynamic Jenkins Pipeline
        │
        ├── Build Application
        ├── Run Tests
        ├── Build Docker Image
        └── Update Kubernetes Manifest
        │
        ▼
GitHub Repository
        │
        ▼
ArgoCD
        │
        ▼
Kubernetes Cluster
```

---

# Core Components

## 1. AI-IDP Platform API

The main FastAPI backend responsible for:

- Service onboarding
- Metadata storage
- Template generation
- Jenkinsfile generation
- Future AI-driven automation

### Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Jinja2
- Kubernetes

---

## 2. PostgreSQL Database

Stores platform metadata such as:

- Service name
- Team name
- Runtime
- Docker build configuration
- Future deployment metadata

Example:

```json
{
  "service_name": "payment-service",
  "team_name": "payments",
  "runtime": "python",
  "docker_build": true
}
```

---

## 3. Platform Shared Library

A centralized Jenkins Shared Library that contains reusable CI/CD logic.

Instead of every repository maintaining large Jenkinsfiles, developers only use:

```groovy
@Library('platform-shared-library') _

platformPipeline()
```

The shared library dynamically:

- Reads metadata from platform.yaml
- Selects runtime-specific build containers
- Runs builds and tests
- Builds Docker images
- Standardizes CI/CD workflows

---

## 4. Dynamic Jenkins Agents

The platform dynamically creates Kubernetes-based Jenkins agents depending on application runtime.

### Python Applications

```yaml
image: python:3.12
```

### NodeJS Applications

```yaml
image: node:20
```

### Java Applications

```yaml
image: maven:3.9.6-eclipse-temurin-17
```

This approach ensures:

- Runtime isolation
- Better scalability
- Reduced dependency conflicts
- Cloud-native CI/CD execution

---

# GitOps Workflow

The platform follows GitOps principles.

## Workflow

1. Developer pushes code
2. GitHub webhook triggers Jenkins
3. Jenkins Shared Library executes pipeline
4. Docker image is built and pushed
5. Kubernetes deployment manifests are updated
6. GitHub repository receives manifest update
7. ArgoCD detects Git changes
8. Kubernetes cluster automatically syncs
9. Application gets deployed

---

# Dynamic Metadata Flow

Each developer repository contains:

```yaml
platform.yaml
```

Example:

```yaml
platform:

  language: python

pipeline:

  build: true

  test: true

  dockerBuild: true

registry:

  repository: saksham8000/payment-service

docker:

  imageTag: latest
```

The shared library reads this metadata and dynamically configures the CI/CD workflow.

---

# AI Agent Workflow (Future Scope)

Currently, AI automation is partially designed but not fully implemented.

Future AI agents will:

## 1. Repository Analysis Agent

Automatically detect:

- Runtime
- Framework
- Build system
- Dependency manager

Example:

- requirements.txt → Python
- pom.xml → Java
- package.json → NodeJS

---

## 2. Pipeline Generation Agent

Generate:

- Jenkinsfiles
- Dockerfiles
- Helm values
- Kubernetes manifests

based on repository structure.

---

## 3. Deployment Recommendation Agent

Suggest:

- CPU limits
- Memory limits
- Replica count
- Autoscaling configuration
- Health probes

using application profiling.

---

## 4. Security Agent

Future integration plans:

- Image scanning
- Secret detection
- Dependency vulnerability analysis
- Policy validation

---

# API Endpoints

## Create Service

```http
POST /service
```

Registers a new service in the platform database.

---

## Get All Services

```http
GET /services
```

Returns all onboarded services.

---

## Get Single Service

```http
GET /service/{service_id}
```

Returns metadata for a specific service.

---

## Generate Values File

```http
GET /generate-values/{service_id}
```

Generates Helm values dynamically using Jinja2 templates.

---

## Generate Jenkinsfile

```http
GET /generate-jenkinsfile/{service_id}
```

Generates platform-integrated Jenkinsfile.

---

# Repository Structure

```text
ai-idp-platform/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schema.py
│   ├── database.py
│   └── templates/
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── postgres.yaml
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Example Developer Repository

```text
payment-service/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── platform.yaml
└── Jenkinsfile
```

Jenkinsfile:

```groovy
@Library('platform-shared-library') _

platformPipeline()
```

---

# Platform Features

- Dynamic Kubernetes Jenkins agents
- Shared CI/CD library
- Metadata-driven automation
- GitOps deployment flow
- Docker image automation
- PostgreSQL metadata storage
- FastAPI backend platform
- Kubernetes-native architecture
- ArgoCD integration
- Runtime-aware pipelines

---

# Current Limitations

- AI agents are partially designed
- No autoscaling automation yet
- No authentication layer
- No RBAC implementation
- No multi-cluster support
- No secret management integration
- Limited deployment strategies

---

# Future Enhancements

- AI-based service onboarding
- Automatic Dockerfile generation
- Automatic Helm chart generation
- Terraform integration
- Vault integration
- Kubernetes policy engine
- Cost optimization agent
- Multi-cloud support
- Self-service developer portal
- AI troubleshooting assistant

---

# Learning Outcomes

This project demonstrates practical understanding of:

- Platform Engineering
- Kubernetes
- Jenkins Shared Libraries
- GitOps
- ArgoCD
- CI/CD automation
- FastAPI backend development
- PostgreSQL integration
- Cloud-native architecture
- Dynamic infrastructure workflows

---

# How Other Repositories Use This Platform

Every developer repository only needs:

## 1. platform.yaml

Contains metadata for the platform.

## 2. Jenkinsfile

```groovy
@Library('platform-shared-library') _

platformPipeline()
```

The platform automatically handles:

- Build logic
- Test logic
- Docker build
- Deployment automation
- Runtime selection
- CI/CD standards

This reduces developer operational overhead and centralizes DevOps automation.

---

# Author

Saksham Singh Gehlot

Cloud | DevOps | Platform Engineering Enthusiast

