import csv
import logging
import random
import time
from collections import defaultdict

from prometheus_client import Counter, Gauge, Histogram, start_http_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("fly_connectome")


SPIKES_TOTAL = Counter(
    "fly_spikes_total",
    "Суммарное количество спайков конкретного нейрона",
    ["neuron_id"],  # Лейбл для фильтрации по имени нейрона
)

SIGNAL_LATENCY = Histogram(
    "fly_signal_latency_seconds",
    "Время прохождения сигнала от входа до моторного выхода",
    buckets=(0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2),  # Границы корзин в секундах
)

ACTIVE_NEURONS = Gauge(
    "fly_active_neurons",
    "Количество нейронов, сработавших за последний залп импульса",
)

def load_connectome(filepath: str):
    graph = defaultdict(list)
    all_sources = set()
    all_targets = set()

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["source_neuron"].strip()
            tgt = row["target_neuron"].strip()
            weight = float(row["weight"].strip())

            graph[src].append((tgt, weight))
            all_sources.add(src)
            all_targets.add(tgt)

    input_nodes = all_sources - all_targets
    terminal_nodes = all_targets - all_sources
    return graph, input_nodes, terminal_nodes

def simulate_wave(graph, input_nodes, terminal_nodes, layer_delay_ms=15):
    
    sample_size = random.randint(1, 2)
    current_layer = set(random.sample(list(input_nodes), sample_size))

    start_time = time.perf_counter()
    all_wave_neurons = set()

    while current_layer:
        
        for neuron in current_layer:
            SPIKES_TOTAL.labels(neuron_id=neuron).inc()  # +1 в счетчик этого нейрона
            all_wave_neurons.add(neuron)

            
            if neuron in terminal_nodes:
                latency = time.perf_counter() - start_time
                SIGNAL_LATENCY.observe(latency)

        
        next_layer = set()
        for neuron in current_layer:
            for target, weight in graph.get(neuron, []):
                if random.random() <= weight:
                    next_layer.add(target)

        if next_layer:
            time.sleep(layer_delay_ms / 1000.0)

        current_layer = next_layer

    
    ACTIVE_NEURONS.set(len(all_wave_neurons))
    logger.info(f"Залп завершен. Активных нейронов: {len(all_wave_neurons)}")

if __name__ == "__main__":
    PORT = 8000
    # Запускаем HTTP-сервер Prometheus в отдельном фоновом потоке
    start_http_server(PORT)
    logger.info(f"Сервер метрик запущен: http://localhost:{PORT}/metrics")

    graph, inputs, terminals = load_connectome("synapses.csv")

    logger.info("Старт бесконечного цикла стимуляции коннектома...")
    # Бесконечный цикл с паузой в 1 секунду между раздражениями
    while True:
        simulate_wave(graph, inputs, terminals)
        time.sleep(1.0)
