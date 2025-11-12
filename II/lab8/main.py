import heapq
import time
import random
import itertools
import matplotlib.pyplot as plt
from collections import deque
from typing import List, Tuple, Dict, Set


# -----------------------------
# Класс состояния склада
# -----------------------------
class WarehouseState:
    def __init__(self, robot_pos: Tuple[int, int], boxes: Set[Tuple[int, int]]):
        self.robot_pos = robot_pos
        self.boxes = frozenset(boxes)

    def __eq__(self, other):
        return self.robot_pos == other.robot_pos and self.boxes == other.boxes

    def __hash__(self):
        return hash((self.robot_pos, self.boxes))

    def __repr__(self):
        return f"Robot: {self.robot_pos}, Boxes: {sorted(self.boxes)}"


# -----------------------------
# Окружение склада
# -----------------------------
class WarehouseEnvironment:
    def __init__(self, width: int, height: int, obstacles: Set[Tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacles = obstacles

    def in_bounds(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos: Tuple[int, int]) -> bool:
        return pos not in self.obstacles

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        (x, y) = pos
        results = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return list(results)

    def get_successor_states(self, state: WarehouseState) -> List[Tuple[WarehouseState, str]]:
        successors = []
        for nx, ny in self.get_neighbors(state.robot_pos):
            new_state = WarehouseState((nx, ny), set(state.boxes))
            successors.append((new_state, f"Move to {(nx, ny)}"))
        return successors

    def get_predecessor_states(self, state: WarehouseState) -> List[Tuple[WarehouseState, str]]:
        # Для обратного поиска просто используем соседей
        predecessors = []
        for nx, ny in self.get_neighbors(state.robot_pos):
            new_state = WarehouseState((nx, ny), set(state.boxes))
            predecessors.append((new_state, f"Move from {(nx, ny)}"))
        return predecessors


# -----------------------------
# Поисковый агент
# -----------------------------
class SearchAlgorithm:
    def __init__(self, environment: WarehouseEnvironment):
        self.env = environment
        self.nodes_visited = 0
        self.execution_time = 0

    # Эвристики
    def heuristic_h1(self, state: WarehouseState, goal_state: WarehouseState) -> float:
        # Манхэттенское расстояние
        return abs(state.robot_pos[0] - goal_state.robot_pos[0]) + abs(state.robot_pos[1] - goal_state.robot_pos[1])

    def heuristic_h2(self, state: WarehouseState, goal_state: WarehouseState) -> float:
        # Евклидово расстояние
        dx = state.robot_pos[0] - goal_state.robot_pos[0]
        dy = state.robot_pos[1] - goal_state.robot_pos[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    # -----------------------------
    # Прямой поиск
    # -----------------------------
    def forward_search(self, initial_state: WarehouseState,
                       goal_state: WarehouseState,
                       use_heuristic: bool = False) -> Tuple[List, int, float]:
        start_time = time.time()
        self.nodes_visited = 0
        counter = itertools.count()  # уникальный счётчик

        if use_heuristic:
            frontier = [(0, next(counter), 0, initial_state, [])]
            cost_so_far = {initial_state: 0}
        else:
            frontier = deque([(initial_state, [])])
            visited = {initial_state}

        while frontier:
            if use_heuristic:
                _, _, g, current_state, path = heapq.heappop(frontier)
            else:
                current_state, path = frontier.popleft()

            self.nodes_visited += 1

            if current_state == goal_state:
                self.execution_time = time.time() - start_time
                return path, len(path), self.execution_time

            for next_state, action in self.env.get_successor_states(current_state):
                new_path = path + [action]
                if use_heuristic:
                    new_cost = g + 1
                    if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                        cost_so_far[next_state] = new_cost
                        priority = new_cost + self.heuristic_h2(next_state, goal_state)
                        heapq.heappush(frontier, (priority, next(counter), new_cost, next_state, new_path))
                else:
                    if next_state not in visited:
                        visited.add(next_state)
                        frontier.append((next_state, new_path))

        self.execution_time = time.time() - start_time
        return None, 0, self.execution_time

    # -----------------------------
    # Обратный поиск
    # -----------------------------
    def backward_search(self, initial_state: WarehouseState,
                        goal_state: WarehouseState,
                        use_heuristic: bool = False) -> Tuple[List, int, float]:
        start_time = time.time()
        self.nodes_visited = 0
        counter = itertools.count()  # уникальный счётчик

        if use_heuristic:
            frontier = [(0, next(counter), 0, goal_state, [])]
            cost_so_far = {goal_state: 0}
        else:
            frontier = deque([(goal_state, [])])
            visited = {goal_state}

        while frontier:
            if use_heuristic:
                _, _, g, current_state, path = heapq.heappop(frontier)
            else:
                current_state, path = frontier.popleft()

            self.nodes_visited += 1

            if current_state == initial_state:
                self.execution_time = time.time() - start_time
                return list(reversed(path)), len(path), self.execution_time

            for prev_state, action in self.env.get_predecessor_states(current_state):
                new_path = path + [action]
                if use_heuristic:
                    new_cost = g + 1
                    if prev_state not in cost_so_far or new_cost < cost_so_far[prev_state]:
                        cost_so_far[prev_state] = new_cost
                        priority = new_cost + self.heuristic_h1(prev_state, initial_state)
                        heapq.heappush(frontier, (priority, next(counter), new_cost, prev_state, new_path))
                else:
                    if prev_state not in visited:
                        visited.add(prev_state)
                        frontier.append((prev_state, new_path))

        self.execution_time = time.time() - start_time
        return None, 0, self.execution_time


# -----------------------------
# Проведение экспериментов
# -----------------------------
def run_experiments():
    width, height = 8, 8
    obstacles = {(3, 3), (3, 4), (4, 3), (4, 4)}
    env = WarehouseEnvironment(width, height, obstacles)

    initial_state = WarehouseState((0, 0), {(1, 2), (2, 2)})
    goal_state = WarehouseState((7, 7), {(5, 6), (6, 6)})

    search = SearchAlgorithm(env)
    results = {}

    print("=" * 80)
    print("ЛАБОРАТОРНАЯ РАБОТА №8: ПЛАНИРОВАНИЕ ДЕЙСТВИЙ ИНТЕЛЛЕКТУАЛЬНОГО АГЕНТА")
    print("=" * 80)

    print("\n1. Прямой поиск (BFS) без эвристики...")
    path, depth, exec_time = search.forward_search(initial_state, goal_state, False)
    print(f"   Узлов посещено: {search.nodes_visited}")
    print(f"   Глубина решения: {depth}")
    print(f"   Время: {exec_time:.4f} сек")
    results["Forward BFS"] = (search.nodes_visited, depth, exec_time)

    print("\n2. Прямой поиск (A*) с эвристикой h2...")
    path, depth, exec_time = search.forward_search(initial_state, goal_state, True)
    print(f"   Узлов посещено: {search.nodes_visited}")
    print(f"   Глубина решения: {depth}")
    print(f"   Время: {exec_time:.4f} сек")
    results["Forward A* (h2)"] = (search.nodes_visited, depth, exec_time)

    print("\n3. Обратный поиск (BFS) без эвристики...")
    path, depth, exec_time = search.backward_search(initial_state, goal_state, False)
    print(f"   Узлов посещено: {search.nodes_visited}")
    print(f"   Глубина решения: {depth}")
    print(f"   Время: {exec_time:.4f} сек")
    results["Backward BFS"] = (search.nodes_visited, depth, exec_time)

    print("\n4. Обратный поиск (A*) с эвристикой h1...")
    path, depth, exec_time = search.backward_search(initial_state, goal_state, True)
    print(f"   Узлов посещено: {search.nodes_visited}")
    print(f"   Глубина решения: {depth}")
    print(f"   Время: {exec_time:.4f} сек")
    results["Backward A* (h1)"] = (search.nodes_visited, depth, exec_time)

    return results, len(obstacles)


# -----------------------------
# Визуализация результатов
# -----------------------------
def plot_performance_graph(results: Dict[str, Tuple[int, int, float]]):
    algorithms = list(results.keys())
    visited_nodes = [v[0] for v in results.values()]
    depths = [v[1] for v in results.values()]
    times = [v[2] for v in results.values()]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    fig.suptitle("Сравнение производительности алгоритмов", fontsize=14, fontweight="bold")

    ax1.bar(algorithms, visited_nodes)
    ax1.set_ylabel("Количество посещённых узлов")
    ax1.grid(axis='y', alpha=0.3)

    ax2.bar(algorithms, times)
    ax2.set_ylabel("Время выполнения (сек)")
    ax2.set_xticks(range(len(algorithms)))
    ax2.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=9)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()


# -----------------------------
# Точка входа
# -----------------------------
if __name__ == "__main__":
    results, branching_factor = run_experiments()
    plot_performance_graph(results)
