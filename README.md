# 🪰 Drosophila Connectome Simulator & Observability Stack

Демонстрационный Cloud-Native проект: микросервис на Python, моделирующий динамику распространения спайковых импульсов по биологическому графу коннектома плодовой мушки (Drosophila melanogaster). Сервис контейнеризирован, развёрнут в кластере Kubernetes (Minikube) и охвачен сквозным мониторингом через Prometheus Operator и Grafana.

![Dashboard Preview](image.png)

---

## 🎯 Краткая выжимка для резюме / HR

- Разработка микросервиса (Python): симуляция импульсной передачи по биологическому графу коннектома (слои ORN, PN, KC, MBON, DN) с вычислением латентности синапсов и экспортом метрик OpenMetrics через prometheus_client.
- Контейнеризация и оркестрация (Docker & Kubernetes): упаковка сервиса в Docker-образ, развёртывание в Minikube с декларативным описанием ресурсов (Deployment, ClusterIP Service).
- Инфраструктурный мониторинг (Prometheus Operator): настройка автоматического сбора метрик с подов через Kubernetes Custom Resource Definition (ServiceMonitor).
- Визуализация данных (Grafana & PromQL): дашборд с расчётом скользящих средних частоты спайков, перцентилей задержек (p95 latency) и текущей активности нейронной сети.

---

## 📌 Архитектура решения

[ Synapses CSV ] ──> [ Python Simulator Pod ] ──(Exposes :8000/metrics)
                               ▲
                               │ Scrapes every 5s
                     [ ServiceMonitor (CRD) ]
                               │
                     [ Prometheus Operator ] ──> [ Grafana Dashboard ]

### Биологическая модель графа
Модель использует ориентированный граф синаптических связей (synapses.csv), разделённый на функциональные нейронные слои:
- ORN (Olfactory Receptor Neurons): первичные сенсорные рецепторы.
- PN (Projection Neurons): проекционные нейроны антенальных долей.
- KC (Kenyon Cells): клетки грибовидного тела (ассоциативная память и распознавание паттернов).
- MBON (Mushroom Body Output Neurons): выходные конвергентные пути выбора реакции.
- DN (Descending Neurons): нисходящие моторные нейроны команд движения (поворот, прыжок, полёт).

---

## 🛠 Технологический стек

- Среда и оркестрация: Linux (Ubuntu), Kubernetes (Minikube)
- Бэкенд: Python 3.11, prometheus_client
- Контейнеризация: Docker
- Сбор метрик: CoreOS Prometheus Operator (ServiceMonitor CRD)
- Визуализация: Grafana (Time Series, Gauge, PromQL)

---

## 📊 Экспортируемые метрики

Микросервис публикует телеметрию на эндпоинте /metrics:

- fly_spikes_total (Counter) — общий счётчик спайков с лейблами нейронов (neuron_id).
- fly_active_neurons (Gauge) — количество активных нейронов в текущей волне импульса.
- fly_signal_latency_seconds (Histogram) — распределение задержек прохождения сигнала по синапсам.

---

## 🚀 Инструкция по развёртыванию

1. Сборка контейнера в локальный реестр Minikube:
minikube image build -t fly-connectome:v1 .

2. Деплой сервиса и регистрация в Prometheus Operator:
minikube kubectl – apply -f deployment.yaml
minikube kubectl – apply -f servicemonitor.yaml

3. Проброс порта веб-интерфейса Grafana:
minikube kubectl – port-forward --address 0.0.0.0 svc/my-release-grafana 3000:80

- URL: http://localhost:3000
- Логин: admin
- Пароль: prom-operator

---

## 📈 Ключевые PromQL-запросы

- Частота спайков по нейронам:
sum by (neuron_id) (rate(fly_spikes_total[1m]))

- Перцентиль задержки волны (p95):
histogram_quantile(0.95, sum(rate(fly_signal_latency_seconds_bucket[5m])) by (le))
