# Cloud Computing Assignment 2 – Kafka-based Event-Driven System

**Student:** Mustafa Fahimy  
**Course:** Cloud Computing (WS2024/25)  
**University of Vienna**

---

## Project Structure

```code
a2/
*project files.
..
├── consumer/
│ ├── consumer-configmap.yaml
│ ├── consumer-deployment.yaml
│ ├── consumer-service.yaml
│ └── consumer.py
│ ├── Dockerfile
│ ├── lims-ingress.yaml
│ ├── README.md
│ ├── requirements.txt
*project files.

```

---

## Overall Solution

This project extends the **Leaf Image Management System (LIMS)** with an **event-driven consumer service**:

- **Task 1 (Local)**:

  - Deployed LIMS locally with Minikube.
  - Implemented a Kafka consumer that ingests image events and stores them in the Consumer MongoDB.
  - Verified end-to-end data flow (Camera → Kafka → Consumer → MongoDB).

- **Task 2 (GKE)**:

  - Deployed the system on Google Kubernetes Engine.
  - Configured **Ingress** as the only external entry point.
  - Exposed REST endpoints (`/image-plant/{type}/{id}`, `/image-plant/{type}/total`) via FastAPI.

- **Task 3 (Metrics)**:
  - Deployed Prometheus + Grafana in the `metrics` namespace.
  - Imported the provided dashboard JSON.
  - Compared **stream (Image API)** vs **batch (DB Synchronizer)** bandwidth.
  - Observed smoother, continuous throughput for stream vs stepwise spikes for batch.

---

## Key Takeaways

- Stream processing provides **low latency and consistent bandwidth**, ideal for real-time workloads.
- Batch processing introduces **latency and bandwidth spikes**, less efficient for responsiveness.
- Kubernetes and GKE enable **scalable, cloud-native deployment**.
- Prometheus + Grafana provide **observability and performance insights**.

---
