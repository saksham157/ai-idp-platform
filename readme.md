
# AI-IDP-Platform

AI-IDP-Platform is a metadata-driven Internal Developer Platform (IDP) built on Kubernetes.

The platform automates:
- CI/CD onboarding
- Jenkins pipeline generation
- Docker image build automation
- GitOps deployment workflows
- Helm-based deployment architecture
- Multi-team platform orchestration

---

# Architecture

Developer Flow:

Developer Repository
↓
Developer pushes application code + platform metadata
↓
AI-IDP-Platform reads metadata
↓
Platform generates:
- Jenkinsfile
- values.yaml
↓
Generated files pushed into repository
↓
GitHub Webhook triggers Jenkins
↓
Jenkins Shared Library executes CI/CD pipeline
↓
Docker image pushed to DockerHub
↓
ArgoCD detects changes
↓
Application deployed into Kubernetes

---

# Core Components

## Control Plane
- FastAPI
- PostgreSQL
- Metadata APIs
- Template generation engine

## CI/CD
- Jenkins
- Jenkins Shared Library
- Dynamic Kubernetes Agents

## GitOps
- ArgoCD
- Helm
- Kubernetes

## Container Runtime
- Docker
- DockerHub Registry

---

# Features

- Metadata-driven onboarding
- Centralized Jenkinsfile generation
- Shared CI/CD logic
- GitOps deployment model
- Kubernetes-native runtime
- Helm-ready deployment architecture
- Multi-team scalable design
- Platform automation APIs

---

# Repository Structure

```text
ai-idp-platform/

├── app/
├── templates/
│   ├── Jenkinsfile.j2
│   ├── values.yaml.j2
│   └── service.yaml.j2
│
├── helm-charts/
│   └── python-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── kubernetes/
├── Dockerfile
├── Jenkinsfile
└── requirements.txt