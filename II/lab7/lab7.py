import math
import time
from collections import deque
from itertools import permutations
import heapq

class TSPSolver:
    
    def __init__(self, cities):
        """
        cities: список кортежей (x, y) - координаты городов
        """
        self.cities = cities
        self.n = len(cities)
        self.dist_matrix = self._create_distance_matrix()
        self.stats = {}
        
    def _create_distance_matrix(self):
        """Создание матрицы расстояний между городами"""
        matrix = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    dx = self.cities[i][0] - self.cities[j][0]
                    dy = self.cities[i][1] - self.cities[j][1]
                    matrix[i][j] = math.sqrt(dx * dx + dy * dy)
        return matrix
    
    def _calculate_path_length(self, path):
        """Вычисление длины маршрута"""
        length = 0
        for i in range(len(path) - 1):
            length += self.dist_matrix[path[i]][path[i + 1]]
        # Возврат в начальный город
        length += self.dist_matrix[path[-1]][path[0]]
        return length
    
    def _is_complete_path(self, path):
        """Проверка, что посещены все города"""
        return len(path) == self.n
    
    def _get_unvisited_cities(self, path):
        """Получить список непосещённых городов"""
        visited = set(path)
        return [i for i in range(self.n) if i not in visited]
    
    # ============ СТРАТЕГИЯ 1: ПОИСК В ШИРИНУ (BFS) ============
    def bfs_search(self, start_city=0):
        """
        Поиск в ширину (BFS) для задачи коммивояжёра
        
        Состояние: кортеж посещённых городов
        Начальное состояние: (start_city,)
        Целевое состояние: любой путь длины n, включающий все города
        """
        print("\n=== ПОИСК В ШИРИНУ (BFS) ===")
        start_time = time.time()
        
        # Очередь: [(путь, длина_пути)]
        queue = deque([([start_city], 0)])
        visited_states = set()
        visited_states.add((start_city,))
        
        nodes_visited = 0
        best_path = None
        best_length = float('inf')
        
        while queue:
            current_path, current_length = queue.popleft()
            nodes_visited += 1
            
            # Проверка целевого состояния
            if self._is_complete_path(current_path):
                total_length = current_length + self.dist_matrix[current_path[-1]][start_city]
                if total_length < best_length:
                    best_length = total_length
                    best_path = current_path + [start_city]
                continue
            
            # Генерация новых состояний
            unvisited = self._get_unvisited_cities(current_path)
            for next_city in unvisited:
                new_path = current_path + [next_city]
                state_tuple = tuple(sorted(new_path))
                
                if state_tuple not in visited_states:
                    visited_states.add(state_tuple)
                    new_length = current_length + self.dist_matrix[current_path[-1]][next_city]
                    queue.append((new_path, new_length))
        
        end_time = time.time()
        
        self.stats['bfs'] = {
            'time': end_time - start_time,
            'nodes_visited': nodes_visited,
            'path_length': best_length,
            'path': best_path
        }
        
        print(f"Лучший путь: {best_path}")
        print(f"Длина пути: {best_length:.2f}")
        print(f"Посещено узлов: {nodes_visited}")
        print(f"Время выполнения: {end_time - start_time:.4f} сек")
        
        return best_path, best_length
    
    # ============ СТРАТЕГИЯ 1: ПОИСК В ГЛУБИНУ (DFS) ============
    def dfs_search(self, start_city=0):
        """
        Поиск в глубину (DFS) для задачи коммивояжёра
        """
        print("\n=== ПОИСК В ГЛУБИНУ (DFS) ===")
        start_time = time.time()
        
        # Стек: [(путь, длина_пути)]
        stack = [([start_city], 0)]
        visited_states = set()
        
        nodes_visited = 0
        best_path = None
        best_length = float('inf')
        
        while stack:
            current_path, current_length = stack.pop()
            nodes_visited += 1
            
            state_tuple = tuple(sorted(current_path))
            if state_tuple in visited_states:
                continue
            visited_states.add(state_tuple)
            
            # Проверка целевого состояния
            if self._is_complete_path(current_path):
                total_length = current_length + self.dist_matrix[current_path[-1]][start_city]
                if total_length < best_length:
                    best_length = total_length
                    best_path = current_path + [start_city]
                continue
            
            # Генерация новых состояний (в обратном порядке для правильного DFS)
            unvisited = self._get_unvisited_cities(current_path)
            for next_city in reversed(unvisited):
                new_path = current_path + [next_city]
                new_length = current_length + self.dist_matrix[current_path[-1]][next_city]
                stack.append((new_path, new_length))
        
        end_time = time.time()
        
        self.stats['dfs'] = {
            'time': end_time - start_time,
            'nodes_visited': nodes_visited,
            'path_length': best_length,
            'path': best_path
        }
        
        print(f"Лучший путь: {best_path}")
        print(f"Длина пути: {best_length:.2f}")
        print(f"Посещено узлов: {nodes_visited}")
        print(f"Время выполнения: {end_time - start_time:.4f} сек")
        
        return best_path, best_length
    
    # ============ ЭВРИСТИЧЕСКАЯ ФУНКЦИЯ ============
    def heuristic_nearest_unvisited(self, current_city, unvisited):
        """
        Эвристика: сумма расстояний до ближайших непосещённых городов
        """
        if not unvisited:
            return 0
        
        # Минимальное остовное дерево (приближённая оценка)
        total = 0
        remaining = list(unvisited)
        
        # Расстояние от текущего города до ближайшего непосещённого
        min_dist = min(self.dist_matrix[current_city][city] for city in remaining)
        total += min_dist
        
        # Примерная оценка оставшегося пути
        while len(remaining) > 1:
            min_edge = float('inf')
            for i in range(len(remaining)):
                for j in range(i + 1, len(remaining)):
                    min_edge = min(min_edge, self.dist_matrix[remaining[i]][remaining[j]])
            total += min_edge
            remaining.pop()
        
        return total
    
    # ============ СТРАТЕГИЯ 2: A* ПОИСК ============
    def astar_search(self, start_city=0):
        """
        A* поиск для задачи коммивояжёра
        f(n) = g(n) + h(n)
        g(n) - стоимость пути от начала
        h(n) - эвристическая оценка до цели
        """
        print("\n=== A* ПОИСК ===")
        start_time = time.time()
        
        # Приоритетная очередь: (f_score, g_score, путь)
        heap = [(0, 0, [start_city])]
        visited_states = {}
        
        nodes_visited = 0
        best_path = None
        best_length = float('inf')
        
        while heap:
            f_score, g_score, current_path = heapq.heappop(heap)
            nodes_visited += 1
            
            state_tuple = tuple(sorted(current_path))
            
            # Пропуск, если уже нашли лучший путь к этому состоянию
            if state_tuple in visited_states and visited_states[state_tuple] <= g_score:
                continue
            visited_states[state_tuple] = g_score
            
            # Проверка целевого состояния
            if self._is_complete_path(current_path):
                total_length = g_score + self.dist_matrix[current_path[-1]][start_city]
                if total_length < best_length:
                    best_length = total_length
                    best_path = current_path + [start_city]
                continue
            
            # Генерация новых состояний
            unvisited = self._get_unvisited_cities(current_path)
            for next_city in unvisited:
                new_path = current_path + [next_city]
                new_g = g_score + self.dist_matrix[current_path[-1]][next_city]
                
                # Эвристическая оценка
                remaining = [c for c in unvisited if c != next_city]
                h_score = self.heuristic_nearest_unvisited(next_city, remaining)
                new_f = new_g + h_score
                
                heapq.heappush(heap, (new_f, new_g, new_path))
        
        end_time = time.time()
        
        self.stats['astar'] = {
            'time': end_time - start_time,
            'nodes_visited': nodes_visited,
            'path_length': best_length,
            'path': best_path
        }
        
        print(f"Лучший путь: {best_path}")
        print(f"Длина пути: {best_length:.2f}")
        print(f"Посещено узлов: {nodes_visited}")
        print(f"Время выполнения: {end_time - start_time:.4f} сек")
        
        return best_path, best_length
    
    # ============ СТРАТЕГИЯ 2: ЖАДНЫЙ ПОИСК ============
    def greedy_search(self, start_city=0):
        """
        Жадный поиск: всегда выбирать ближайший непосещённый город
        """
        print("\n=== ЖАДНЫЙ ПОИСК ===")
        start_time = time.time()
        
        current_city = start_city
        path = [current_city]
        unvisited = set(range(self.n)) - {current_city}
        total_length = 0
        nodes_visited = 1
        
        while unvisited:
            # Найти ближайший непосещённый город
            nearest = min(unvisited, key=lambda city: self.dist_matrix[current_city][city])
            total_length += self.dist_matrix[current_city][nearest]
            current_city = nearest
            path.append(current_city)
            unvisited.remove(current_city)
            nodes_visited += 1
        
        # Возврат в начальный город
        total_length += self.dist_matrix[current_city][start_city]
        path.append(start_city)
        
        end_time = time.time()
        
        self.stats['greedy'] = {
            'time': end_time - start_time,
            'nodes_visited': nodes_visited,
            'path_length': total_length,
            'path': path
        }
        
        print(f"Найденный путь: {path}")
        print(f"Длина пути: {total_length:.2f}")
        print(f"Посещено узлов: {nodes_visited}")
        print(f"Время выполнения: {end_time - start_time:.4f} сек")
        
        return path, total_length
    
    # ============ ОБРАТНЫЙ ПОИСК ============
    def backward_search(self, start_city=0):
        """
        Обратный поиск: начинаем с полного маршрута и удаляем города
        """
        print("\n=== ОБРАТНЫЙ ПОИСК ===")
        start_time = time.time()
        
        # Начинаем с любого полного маршрута
        all_cities = list(range(self.n))
        current_path = all_cities + [start_city]
        current_length = self._calculate_path_length(all_cities)
        
        improved = True
        iterations = 0
        
        # 2-opt оптимизация (обратный поиск через улучшение)
        while improved:
            improved = False
            iterations += 1
            
            for i in range(1, self.n - 1):
                for j in range(i + 1, self.n):
                    # Пробуем обратить сегмент пути
                    new_path = current_path[:i] + current_path[i:j+1][::-1] + current_path[j+1:]
                    new_length = self._calculate_path_length(new_path[:-1])
                    
                    if new_length < current_length:
                        current_path = new_path
                        current_length = new_length
                        improved = True
                        break
                
                if improved:
                    break
        
        end_time = time.time()
        
        self.stats['backward'] = {
            'time': end_time - start_time,
            'iterations': iterations,
            'path_length': current_length,
            'path': current_path
        }
        
        print(f"Оптимизированный путь: {current_path}")
        print(f"Длина пути: {current_length:.2f}")
        print(f"Итераций: {iterations}")
        print(f"Время выполнения: {end_time - start_time:.4f} сек")
        
        return current_path, current_length
    
    # ============ СРАВНЕНИЕ СТРАТЕГИЙ ============
    def compare_strategies(self):
        """Вывод сравнительной таблицы"""
        print("\n" + "="*80)
        print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ СТРАТЕГИЙ")
        print("="*80)
        print(f"{'Стратегия':<20} {'Время (сек)':<15} {'Узлов':<15} {'Длина пути':<15} {'Оптимальность'}")
        print("-"*80)
        
        for name, stats in self.stats.items():
            strategy_names = {
                'bfs': 'Поиск в ширину',
                'dfs': 'Поиск в глубину',
                'astar': 'A* поиск',
                'greedy': 'Жадный поиск',
                'backward': 'Обратный поиск'
            }
            
            nodes = stats.get('nodes_visited', stats.get('iterations', '-'))
            optimal = "✓" if stats['path_length'] == min(s['path_length'] for s in self.stats.values()) else "–"
            
            print(f"{strategy_names[name]:<20} {stats['time']:<15.4f} {nodes:<15} {stats['path_length']:<15.2f} {optimal}")
        
        print("="*80)
    
    def visualize_solution(self, path):
        """Визуализация решения (текстовая)"""
        print("\n=== ВИЗУАЛИЗАЦИЯ МАРШРУТА ===")
        print("Последовательность посещения городов:")
        for i, city in enumerate(path):
            if i < len(path) - 1:
                print(f"  Город {city} → Город {path[i+1]} (расстояние: {self.dist_matrix[city][path[i+1]]:.2f})")
            else:
                print(f"  [Завершение маршрута]")


# ============ ПРИМЕР ИСПОЛЬЗОВАНИЯ ============
if __name__ == "__main__":
    print("ЛАБОРАТОРНАЯ РАБОТА №7")
    print("ЗАДАЧА КОММИВОЯЖЁРА")
    print("="*80)
    
    # Определение городов (координаты)
    cities = [
        (0, 0),    # Город 0
        (10, 15),  # Город 1
        (20, 5),   # Город 2
        (15, 25),  # Город 3
        (30, 20),  # Город 4
        (25, 10)   # Город 5
    ]
    
    print(f"\nКоличество городов: {len(cities)}")
    print("Координаты городов:")
    for i, (x, y) in enumerate(cities):
        print(f"  Город {i}: ({x}, {y})")
    
    # Создание решателя
    solver = TSPSolver(cities)
    
    print("\n" + "="*80)
    print("МАТРИЦА РАССТОЯНИЙ")
    print("="*80)
    for i in range(solver.n):
        print(f"Город {i}: ", end="")
        for j in range(solver.n):
            print(f"{solver.dist_matrix[i][j]:6.2f}", end=" ")
        print()
    
    # Запуск всех стратегий
    start_city = 0
    
    # 1. BFS
    solver.bfs_search(start_city)
    
    # 2. DFS
    solver.dfs_search(start_city)
    
    # 3. Жадный поиск
    solver.greedy_search(start_city)
    
    # 4. A* поиск
    solver.astar_search(start_city)
    
    # 5. Обратный поиск
    solver.backward_search(start_city)
    
    # Сравнение стратегий
    solver.compare_strategies()
    
    # Визуализация лучшего решения
    best_strategy = min(solver.stats.items(), key=lambda x: x[1]['path_length'])
    print(f"\n\nЛУЧШАЯ СТРАТЕГИЯ: {best_strategy[0].upper()}")
    solver.visualize_solution(best_strategy[1]['path'])