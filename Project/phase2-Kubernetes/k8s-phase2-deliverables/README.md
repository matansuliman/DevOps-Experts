# Phase 2: Orchestration - Kubernetes Basics & Advanced

This folder contains Kubernetes manifests to deploy a scalable, highly available web application on **Docker Desktop Kubernetes**.

> Adjust names, images, and env according to your app from Part 1.

## Contents
- `namespace.yaml`
- `configmap.yaml`
- `secret.yaml` (uses `stringData` for convenience during dev)
- `deployment.yaml` (with **readiness** and **liveness** probes)
- `service.yaml` (NodePort for external access on Docker Desktop)
- `hpa.yaml` (CPU/Memory based autoscaling)
- `cronjob.yaml` (periodic health check from inside the cluster)

## Prerequisites
- Docker Desktop with **Kubernetes** enabled
- kubectl installed and pointing to Docker Desktop context
- Your application image built from Phase 1 (e.g., `matan/legi-bit:1.0.0`), or any other image accessible by Docker Desktop

## Quickstart
```bash
# 1) Verify Kubernetes is enabled
kubectl config current-context
kubectl get nodes

# 2) Apply manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
kubectl apply -f cronjob.yaml

# 3) Check resources
kubectl -n myapp get all
kubectl -n myapp get hpa
kubectl -n myapp get jobs

# 4) Access the app (NodePort)
# On Docker Desktop (Windows): http://localhost:30080
# Or port-forward if you prefer:
kubectl -n myapp port-forward svc/myapp 8080:8080
# Then open http://localhost:8080
```

## Replace Image & Ports
- Edit `deployment.yaml`:
  - `image: "matan/legi-bit:1.0.0"` → your image from Part 1
  - `containerPort: 8080` → your app's listening port
- Edit `service.yaml`:
  - `port: 8080` and `targetPort: http` should match your container port
  - `nodePort: 30080` can be changed if occupied

## Probes (בריאות)
- **Readiness** probe checks `/` so traffic is sent only when the pod is ready.
- **Liveness** probe checks `/` to restart unhealthy pods.
- If your app exposes a dedicated `/healthz`, change the probe paths accordingly.

## HPA (Autoscaling)
- Requires resource requests/limits in the deployment.
- Scales between 2 and 5 replicas based on CPU (60%) and memory (70%).

## CronJob (בקרת שרות)
- Runs every minute and calls the Service inside the cluster (`myapp.myapp.svc.cluster.local:8080/`).
- Exits with non‑zero code if it doesn't get HTTP 200 → Job shows as failed.

## Cleanup
```bash
kubectl delete -f cronjob.yaml
kubectl delete -f hpa.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f secret.yaml
kubectl delete -f configmap.yaml
kubectl delete -f namespace.yaml
```

## Notes
- Using `NodePort` is simplest on Docker Desktop. If you prefer Ingress, install an ingress controller (e.g., NGINX Ingress) and swap `service.yaml` to `ClusterIP` plus an `Ingress` manifest.
- Secrets in `stringData` are for dev. In prod, consider sealed-secrets or an external secret manager.
- For CPU-based scaling, generate load (e.g., `hey` or `ab`) to see HPA in action.

---

Generated on 2025-09-21T10:54:04
