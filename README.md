# 📘 JDC Cabanga — Automated Daily School Diary Collector

A fully automated system that retrieves **"Journal de Classe" (school diary)** data from my daughter's school application (Cabanga) and sends a **daily email summary** of lessons, tests, and assignments.

The purpose of this project is to demonstrate a complete DevOps pipeline, including containerization, CI/CD, secure secrets handling, and Kubernetes automation on a Raspberry Pi K3s cluster.

---

## 🚀 Features

- Fetches Cabanga diary entries for the next 14 days  
- Sends daily email report (SMTP) with lessons & tests  
- Secure token refresh via API  
- Runs automatically via **Kubernetes CronJob**  
- Built & deployed through **Jenkins CI/CD**  
- Multi-arch Docker image for AMD64 + ARM64  
- Hosted on **K3s Raspberry Pi cluster**  
- Uses **GitHub Container Registry (GHCR)** as Docker registry  

---

# 🏗️ Architecture Overview

The system is composed of:

- **GitHub** — holds application source code  
- **Jenkins** — builds and deploys the container  
- **GHCR** — stores multi-arch Docker images  
- **K3s Cluster** — runs CronJob and sends email  
- **Kubernetes Secrets** — store API tokens and email credentials  

## 🔧 High-Level Architecture

```mermaid
flowchart LR
    A[GitHub Repository] -->|SCM Polling| B[Jenkins CI/CD]
    B -->|Buildx multi-arch build| C[GitHub Container Registry]
    C -->|ARM64 Pull| D[K3s Cluster (Raspberry Pi)]
    D --> E[Kubernetes CronJob]
    E --> F[Python App Execution]
    F --> G[Daily Email Report]
```

# 🙌 Author

Bruno Henrard

GitHub: https://github.com/henrardb

