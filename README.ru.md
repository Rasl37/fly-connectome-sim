[English](README.md) | [Русский](README.ru.md)

# Симулятор коннектома Drosophila и стек наблюдаемости

Демонстрационный Cloud-Native проект: микросервис на Python, моделирующий динамику распространения спайковых импульсов по биологическому графу связей плодовой мушки (*Drosophila melanogaster*). Сервис упакован в Docker-контейнер, развернут в локальном кластере Kubernetes (Minikube) и охвачен мониторингом через Prometheus Operator и Grafana.

![Dashboard Preview](image.png)

## Обзор проекта
* **Микросервис (Python):** Симулирует импульсную передачу по слоям биологического графа (ORN, PN, KC, MBON, DN), вычисляет синаптическую задержку и отдает метрики OpenMetrics через библиотеку `prometheus_client`.
* **Контейнеризация и оркестрация:** Приложение упаковано в Docker и развернуто в Minikube через декларативные манифесты (`Deployment`, `ClusterIP Service`).
* **Мониторинг (Prometheus Operator):** Автоматический сбор метрик с подов настроен через Kubernetes Custom Resource Definition (`ServiceMonitor`).
* **Визуализация (Grafana и PromQL):** Дашборд отображает частоту спайков по нейронам, 95-й перцентиль задержки (p95 latency) и кластеры активных нейронов.

## Архитектура

```text
[ Synapses CSV ] ──> [ Python Simulator Pod ] ──(Отдает :8000/metrics)
                             ▲
                             │ Сбор метрик каждые 5с
                    [ ServiceMonitor (CRD) ]
                             │
                  [ Prometheus Operator ] ──> [ Дашборд Grafana ]
```

### Модель графа и используемый стек

Симуляция обрабатывает файл `synapses.csv`, распределенный по функциональным слоям:
* **ORN:** Обонятельные рецепторные нейроны (входной сигнал)
* **PN:** Проекционные нейроны
* **KC:** Клетки Кеньона (распознавание паттернов)
* **MBON:** Выходные нейроны грибовидного тела
* **DN:** Нисходящие нейроны (команды движения)

**Стек технологий:** Python 3.11, Docker, Minikube (Kubernetes), CoreOS Prometheus Operator, Grafana.
