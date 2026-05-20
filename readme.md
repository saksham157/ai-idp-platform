# platform-jenkins-base

A production-grade Jenkins deployment running natively inside a Kubernetes cluster. This project sets up Jenkins as a Kubernetes-native CI/CD engine using the Kubernetes plugin for dynamic ephemeral build agents, webhook-based pipeline triggering, and customized pod templates configured in Jenkins Clouds.

---

## Overview

Traditional Jenkins deployments run as standalone servers with static agents that idle between builds. This project takes a cloud-native approach — Jenkins runs inside the cluster as a Kubernetes workload, and every build gets its own isolated, ephemeral agent pod that spins up on demand and is automatically terminated on completion.

Pipeline execution is triggered via GitHub webhooks, eliminating the need for polling and ensuring near-instant build starts on every push or pull request.

---

## Architecture

```text
Developer pushes code
        │
        ▼
GitHub Webhook
        │
        ▼
Jenkins Controller (Pod — inside Kubernetes)
        │
        ▼
Kubernetes Plugin
        │
        ├── Reads pod template from Clouds configuration
        ├── Provisions ephemeral agent pod in cluster
        └── Assigns build to agent
        │
        ▼
Ephemeral Agent Pod (runs pipeline steps)
        │
        ├── Build
        ├── Test
        ├── Docker image build & push
        └── Update Helm chart / Kubernetes manifest
        │
        ▼
Agent pod auto-deleted on completion
        │
        ▼
ArgoCD detects manifest change in Git
        │
        ▼
Kubernetes cluster synced → Application deployed
```

---

## Core Components

### Jenkins Controller

- Deployed as a Kubernetes `Deployment` inside the cluster
- Exposed via a `Service` for internal access and webhook reception
- Persistent volume attached for Jenkins home data
- Configured with the Kubernetes plugin to communicate with the cluster API

### Kubernetes Plugin

- Connects Jenkins to the Kubernetes API server
- Dynamically provisions agent pods for each build using pod templates defined in **Manage Jenkins → Clouds**
- No static agents — zero idle compute between builds
- Each agent pod is isolated, preventing build contamination across pipelines

### Webhook Triggering

- GitHub webhooks point to the Jenkins controller service endpoint
- Pipelines trigger immediately on `push`, `pull_request`, or tag events
- No SCM polling configured — webhook-only triggering for efficiency and speed

### Pod Templates (Clouds Configuration)

Pod templates are defined in **Manage Jenkins → Clouds → Kubernetes** and customized per use case:

| Template | Container Image | Purpose |
|---|---|---|
| `python-agent` | `python:3.12` | Python application builds and tests |
| `node-agent` | `node:20` | Node.js application builds |
| `maven-agent` | `maven:3.9.6-eclipse-temurin-17` | Java/Maven builds |
| `docker-agent` | `docker:dind` | Docker image build and push |

Each template defines:
- Container image and resource requests/limits
- Environment variables
- Volume mounts (e.g. Docker socket or registry credentials)
- Node selector and tolerations where required

### RBAC

A dedicated `ServiceAccount` is bound to a `Role` granting Jenkins least-privilege access to:
- `create`, `get`, `list`, `delete` pods in the agents namespace
- `get` pod logs
- `create` secrets (for credential injection)

Jenkins does not have cluster-wide permissions.

---

## Repository Structure

```text
platform-jenkins-base/
│
├── kubernetes/
│   ├── namespace.yaml            # Dedicated namespace for Jenkins
│   ├── serviceaccount.yaml       # Jenkins ServiceAccount
│   ├── rbac.yaml                 # Role and RoleBinding
│   ├── deployment.yaml           # Jenkins controller Deployment
│   ├── service.yaml              # ClusterIP / NodePort / Ingress
│   └── pvc.yaml                  # PersistentVolumeClaim for Jenkins home
│
├── pod-templates/
│   ├── python-agent.yaml         # Python build agent template
│   ├── node-agent.yaml           # Node.js build agent template
│   ├── maven-agent.yaml          # Java/Maven build agent template
│   └── docker-agent.yaml         # Docker-in-Docker agent template
│
├── configs/
│   └── jenkins-casc.yaml         # Jenkins Configuration as Code (JCasC)
│
└── README.md
```

---

## How It Works

### 1. Jenkins Starts Inside Kubernetes

Jenkins controller runs as a pod. On startup, the Kubernetes plugin reads the cluster credentials from the in-cluster `ServiceAccount` token — no manual kubeconfig needed.

### 2. Webhook Fires on Code Push

A GitHub webhook sends a `POST` request to the Jenkins controller endpoint. Jenkins identifies the matching pipeline job and queues a build immediately.

### 3. Agent Pod Provisioned from Cloud Template

Jenkins reads the matching pod template from **Clouds** configuration, submits a pod spec to the Kubernetes API, and waits for the agent pod to become `Running`.

### 4. Build Executes Inside Agent Pod

The pipeline steps run entirely inside the agent pod — isolated from other builds and from the Jenkins controller. Credentials are injected as environment variables or mounted secrets.

### 5. Agent Pod Terminated

On build completion (success or failure), the Kubernetes plugin deletes the agent pod. No manual cleanup required.

### 6. ArgoCD Syncs Deployment

If the pipeline updates a Kubernetes manifest or Helm values file in Git, ArgoCD detects the change and syncs the cluster automatically — completing the GitOps loop.

---

## Key Design Decisions

**Webhook over polling** — SCM polling creates unnecessary API calls and adds latency. Webhooks give instant triggering and are more efficient at scale.

**Clouds pod templates over Jenkinsfile agent blocks** — Defining templates centrally in Clouds keeps pipeline code clean and lets platform teams manage agent configurations independently of application repositories. Developers reference a template label; they don't own the container spec.

**Ephemeral agents over persistent agents** — Static agents accumulate state, cached dependencies, and leftover artifacts from previous builds. Ephemeral pods start clean every time, eliminating an entire class of flaky build issues.

**Least-privilege RBAC** — Jenkins only has permission to manage pods in its own namespace. It cannot modify deployments, services, or resources in other namespaces.

---

## Prerequisites

- Kubernetes cluster (tested on EKS)
- `kubectl` configured with cluster access
- Helm (optional, for chart-based deployment)
- GitHub repository with webhook access
- Container registry credentials (Docker Hub, ECR, etc.)

---

## Deployment

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Apply RBAC
kubectl apply -f kubernetes/serviceaccount.yaml
kubectl apply -f kubernetes/rbac.yaml

# Create persistent volume claim
kubectl apply -f kubernetes/pvc.yaml

# Deploy Jenkins controller
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

After Jenkins starts, configure the Kubernetes Cloud under **Manage Jenkins → Clouds → New Cloud → Kubernetes** and apply the pod templates from `pod-templates/`.

---

## Webhook Setup

1. In your GitHub repository, go to **Settings → Webhooks → Add webhook**
2. Set the Payload URL to your Jenkins endpoint: `http://<jenkins-service>/github-webhook/`
3. Set Content type to `application/json`
4. Select the events to trigger on (`push`, `pull_request`, or specific events)
5. In the Jenkins job, enable **GitHub hook trigger for GITScm polling** under Build Triggers

---

## Author

Saksham Singh Gehlot — DevOps & Platform Engineer  
[github.com/saksham157](https://github.com/saksham157)
