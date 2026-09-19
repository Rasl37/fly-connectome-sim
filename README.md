# 🪰 Drosophila Connectome Simulator & Observability Stack

Демонстрационный Cloud-Native проект: микросервис на Python, моделирующий динамику распространения спайковых потенциалов действия по биологическому графу коннектома плодовой мухи (*Drosophila melanogaster*). Сервис контейнеризирован, развёрнут в кластере Kubernetes (Minikube) и охвачен сквозным мониторингом через Prometheus Operator и Grafana.

![Dashboard Preview](image.png)

---

## 📌 Архитектура решения

```text
[ Synapses CSV ] ──> [ Python Simulator Pod ] ──(Exposes :8000/metrics)
                               ▲
                               │ Scrapes every 5s
                     [ ServiceMonitor (CRD) ]
                               │
                     [ Prometheus Operator ] ──> [ Grafana Dashboard ]
